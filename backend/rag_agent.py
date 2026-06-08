"""
rag_agent.py — RAG агент для колл-центра (ChromaDB локально)
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
TOP_K         = 10
MAX_HISTORY   = 10
MIN_SIMILARITY = 0.15  # минимальный порог похожести для fallback
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

SYSTEM_PROMPT = """Ты — интеллектуальный ассистент НПК (Национальная Корпорация Платежей). Твоя задача — помогать операторам быстро находить точную информацию из базы знаний.

ПРАВИЛА:
- Отвечай ТОЛЬКО на основе предоставленного контекста из базы знаний
- Если в контексте есть нужная информация — используй её полностью, даже если вопрос сформулирован иначе
- Если информации недостаточно — задай ОДИН уточняющий вопрос
- Если в контексте есть готовый скрипт — следуй его структуре дословно
- Тон: вежливый, профессиональный, краткий

ВАЖНО: Не говори "информации нет", если в контексте есть хоть какие-то релевантные данные. Попробуй составить ответ из того, что есть.

УТОЧНЯЮЩИЕ ВОПРОСЫ (когда контекст совсем не подходит):
- "подключить услугу" → "Подскажите, какую именно услугу вы хотите подключить?"
- "проблема с тарифом" → "Уточните, пожалуйста, что именно за проблема?"
- "не работает" → "Что именно не работает? Опишите подробнее."

КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ:
{context}"""


def get_embedding(text: str) -> list[float]:
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


def search(query: str) -> str:
    """Embedding search + keyword fallback"""
    emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[emb],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results.get("distances", [[]])[0]

    # Проверяем, есть ли хорошие результаты
    has_good_results = any(d < MIN_SIMILARITY for d in distances) if distances else False

    parts = []
    for i, (doc, meta) in enumerate(zip(docs, metas), 1):
        source = meta.get("source", "")
        parts.append(f"[{i}] Источник: {source}\n{doc}")

    # Fallback: если embedding не нашёл ничего близкого — ищем по ключевым словам
    if not has_good_results:
        keywords = extract_keywords(query)
        if keywords:
            keyword_results = keyword_search(keywords, limit=5)
            if keyword_results:
                parts.append("\n\n[Дополнительно по ключевым словам]\n" + keyword_results)

    return "\n\n---\n\n".join(parts) if parts else "Информация не найдена в базе знаний."


def extract_keywords(text: str) -> list[str]:
    """Извлекает ключевые слова из запроса"""
    # Убираем стоп-слова, оставляем существительные и глаголы
    stop_words = {"как", "что", "где", "когда", "кто", "почему", "зачем",
                  "из", "в", "на", "по", "для", "с", "у", "о", "об",
                  "или", "и", "а", "но", "если", "так", "же", "ли"}
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text.lower())
    return [w for w in words if w not in stop_words and len(w) > 2]


def keyword_search(keywords: list[str], limit: int = 5) -> str:
    """Простой keyword search через полный перебор документов"""
    try:
        all_docs = collection.get(include=["documents", "metadatas"])
        scored = []
        for doc, meta in zip(all_docs["documents"], all_docs["metadatas"]):
            score = sum(1 for kw in keywords if kw in doc.lower())
            if score > 0:
                scored.append((score, doc, meta))

        scored.sort(reverse=True, key=lambda x: x[0])
        parts = []
        for i, (score, doc, meta) in enumerate(scored[:limit], 1):
            source = meta.get("source", "")
            parts.append(f"[{i}] Источник: {source} (совпадений: {score})\n{doc}")
        return "\n\n---\n\n".join(parts)
    except Exception:
        return ""


class RAGAgent:
    def __init__(self):
        self.history: list[dict] = []

    def chat(self, user_message: str) -> str:
        # Улучшенный search query: добавляем контекст из истории для коротких вопросов
        search_query = user_message
        if len(user_message.split()) <= 6 and self.history:
            last_bot = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"),
                ""
            )
            last_user = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "user"),
                ""
            )
            search_query = f"{last_user} {last_bot[:200]} {user_message}"

        context = search(search_query)
        system = {"role": "system", "content": SYSTEM_PROMPT.format(context=context)}
        self.history.append({"role": "user", "content": user_message})
        messages = [system] + self.history[-MAX_HISTORY:]

        resp = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []
