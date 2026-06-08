"""
rag_agent.py -- RAG агент для колл-центра (ChromaDB локально)
"""

import os
import re
from openai import OpenAI
from groq import Groq
import chromadb
from dotenv import load_dotenv

load_dotenv()

# ─── НАСТРОЙКИ ───────────────────────────────────────────────────────────────
COLLECTION    = "callcenter-docs"
CHROMA_FOLDER = "./chroma_db"
EMBED_MODEL   = "text-embedding-3-small"
LLM_MODEL     = "llama-3.3-70b-versatile"
TOP_K         = 4
MAX_HISTORY   = 2
MAX_CONTEXT   = 3800
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

SYSTEM_PROMPT = """Ты -- ассистент НПК (Национальная Корпорация Платежей). Отвечай операторам колл-центра ТОЛЬКО на основе контекста ниже.

ЗАПРЕЩЕНО:
- Говорить "К сожалению, в предоставленном контексте нет информации"
- Говорить "Необходимо уточнить"
- Просить уточнить, если в контексте есть хоть какие-то данные

ОБЯЗАТЕЛЬНО:
- Если в контексте есть релевантная информация -- используй её и дай ответ
- Если контекст частично подходит -- дай ответ на основе того, что есть
- Отвечай чётко и по делу
- Если контекст совсем пуст -- тогда и только тогда скажи: "К сожалению, по этому вопросу информации в базе нет. Уточните у супервайзера."

КОНТЕКСТ:
{context}"""


def get_embedding(text: str) -> list[float]:
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


def _extract_keywords(text: str) -> list[str]:
    """Извлекает значимые ключевые слова из запроса."""
    stop = {"как", "что", "где", "когда", "кто", "почему", "зачем",
            "из", "в", "на", "по", "для", "с", "у", "о", "об",
            "или", "и", "а", "но", "если", "так", "же", "ли", "не",
            "это", "тот", "такой", "который", "быть", "есть", "иметь",
            "между", "при", "до", "после", "от", "до", "про", "со"}
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text.lower())
    return [w for w in words if w not in stop and len(w) > 2]


def _keyword_search(keywords: list[str], limit: int = 3) -> str:
    """Поиск по ключевым словам через полный перебор всех документов."""
    if not keywords:
        return ""
    try:
        all_data = collection.get(include=["documents", "metadatas"])
        docs = all_data.get("documents", [])
        metas = all_data.get("metadatas", [])
        if not docs:
            return ""

        scored = []
        for doc, meta in zip(docs, metas):
            doc_lower = doc.lower()
            # Считаем совпадения ключевых слов
            score = sum(3 for kw in keywords if kw in doc_lower)
            # Бонус за точное совпадение фразы
            for i in range(len(keywords) - 1):
                bigram = f"{keywords[i]} {keywords[i+1]}"
                if bigram in doc_lower:
                    score += 5
            if score > 0:
                scored.append((score, doc, meta))

        scored.sort(reverse=True, key=lambda x: x[0])
        parts = []
        for i, (score, doc, meta) in enumerate(scored[:limit], 1):
            source = meta.get("source", "")
            parts.append(f"[K{i}] {source}\n{doc}")
        return "\n\n---\n\n".join(parts)
    except Exception:
        return ""


def search(query: str) -> str:
    """Embedding search + keyword fallback."""
    # 1. Эмбеддинг-поиск
    emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[emb],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results.get("distances", [[]])[0]

    parts = []
    best_distance = min(distances) if distances else 999

    for i, (doc, meta) in enumerate(zip(docs, metas), 1):
        source = meta.get("source", "")
        parts.append(f"[{i}] {source}\n{doc}")

    # 2. Если embedding дал плохие результаты (дистанция > 0.35) -- добавляем keyword search
    if best_distance > 0.35:
        keywords = _extract_keywords(query)
        kw_results = _keyword_search(keywords, limit=3)
        if kw_results:
            parts.append("\n\n[Дополнительно по ключевым словам]\n" + kw_results)

    return "\n\n---\n\n".join(parts) if parts else ""


class RAGAgent:
    def __init__(self):
        self.history: list[dict] = []

    def chat(self, user_message: str) -> str:
        search_query = user_message
        # Используем историю только для коротких уточняющих вопросов
        if len(user_message.split()) <= 4 and self.history:
            last_user = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "user"), ""
            )
            last_bot = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"), ""
            )
            search_query = f"{last_user} {last_bot[:150]} {user_message}"

        context = search(search_query)
        if len(context) > MAX_CONTEXT:
            context = context[:MAX_CONTEXT] + "\n[...]"

        system = {"role": "system", "content": SYSTEM_PROMPT.format(context=context)}
        self.history.append({"role": "user", "content": user_message})
        messages = [system] + self.history[-MAX_HISTORY:]

        resp = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []
