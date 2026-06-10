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
TOP_K         = 5
MAX_HISTORY   = 10
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

VAGUE_KEYWORDS = {
    "подключить", "услуга", "услуги", "подключение",
    "тариф", "тарифы", "стоимость", "цена",
    "проблема", "не работает", "ошибка", "сбой",
    "как", "что", "где", "когда", "зачем",
}

SYSTEM_PROMPT = """Ты — интеллектуальный ассистент колл-центра НПК. Твоя задача — отвечать на вопросы операторов, используя ТОЛЬКО предоставленный ниже контекст из базы знаний.

ВАЖНЫЕ ПРАВИЛА:
1. Перед ответом внимательно проанализируй контекст: содержит ли он конкретную информацию ПО ТЕМЕ заданного вопроса? Если контекст содержит только общие фразы или данные по другой теме — значит, ответа в базе нет.
2. Если вопрос расплывчатый (например "подключить услугу", "тарифы", "проблема") — задай ОДИН уточняющий вопрос. НЕ отвечай "информации нет" на расплывчатые вопросы — уточни детали.
3. Если в контексте есть таблица/список по ТЕМЕ вопроса — перечисли данные из неё.
4. Если контекст по теме найден, но неполный — дай то, что есть, и уточни что именно нужно дополнить.
5. Если контекст совсем пуст или НЕ содержит ответа на вопрос — скажи: "К сожалению, по этому вопросу информации в базе нет. Уточните у супервайзера."
6. Ты — виртуальный ИИ-помощник, НЕ живой оператор. НЕ называй своё имя, НЕ представляйся человеком и НЕ используй конструкции вроде "меня зовут...".

УТОЧНЯЮЩИЕ ВОПРОСЫ (когда задавать):
- "подключить услугу" → "Подскажите, какую именно услугу вы хотите подключить? (например, ЦОИД, СПБС, СОБС, Антифрод-центр и т.д.)"
- "тарифы" → "По какой именно услуге вас интересуют тарифы?"
- "проблема / не работает" → "Что именно не работает? Опишите проблему подробнее."
- "участники" → "Участники какой системы или услуги вас интересуют?"

ФОРМАТ ОТВЕТА:
- Отвечай чётко и по делу, без лишних вступлений
- Если есть шаги или список — перечисли их
- Если контекст содержит таблицу — перенеси данные из неё в понятный текст
- Тон: вежливый, профессиональный

КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ:
{context}"""


def get_embedding(text: str) -> list[float]:
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


def keyword_search(query: str, n_results: int = 5) -> str:
    """Fallback keyword search in ChromaDB documents."""
    query_lower = query.lower()
    all_docs = collection.get(include=["documents", "metadatas"])
    docs = all_docs.get("documents", [])
    metas = all_docs.get("metadatas", [])

    scored = []
    for doc, meta in zip(docs, metas):
        if not doc:
            continue
        doc_lower = doc.lower()
        score = 0
        for word in query_lower.split():
            if len(word) > 2:
                score += doc_lower.count(word)
        if score > 0:
            scored.append((score, doc, meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    parts = []
    for i, (score, doc, meta) in enumerate(scored[:n_results], 1):
        source = meta.get("source", "") if meta else ""
        parts.append(f"[{i}] Источник: {source}\n{doc}")

    return "\n\n---\n\n".join(parts) if parts else ""


def search(query: str) -> str:
    emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[emb],
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )
    parts = []
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        source = meta.get("source", "")
        parts.append(f"[{i}] Источник: {source}\n{doc}")

    context = "\n\n---\n\n".join(parts) if parts else ""

    # Fallback: if semantic search returns weak results, try keyword
    if not context or len(context) < 300:
        kw = keyword_search(query)
        if kw:
            context = context + "\n\n--- KEYWORD FALLBACK ---\n\n" + kw if context else kw

    return context or "Информация не найдена в базе знаний."


def is_vague(query: str) -> bool:
    """Проверяет, является ли вопрос расплывчатым."""
    q_lower = query.lower().strip()
    words = set(q_lower.split())
    # Если только общие слова без конкретики
    if len(words) <= 3 and any(w in VAGUE_KEYWORDS for w in words):
        return True
    # Если запрос совсем короткий и без именованных сущностей
    if len(q_lower.split()) <= 2:
        return True
    return False


class RAGAgent:
    def __init__(self):
        self.history: list[dict] = []

    def chat(self, user_message: str) -> str:
        # Если вопрос короткий — добавляем контекст из предыдущего ответа
        search_query = user_message
        if len(user_message.split()) <= 5 and self.history:
            last_bot = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"),
                ""
            )
            search_query = f"{last_bot[:300]} {user_message}"

        context = search(search_query)
        system = {"role": "system", "content": SYSTEM_PROMPT.format(context=context)}
        self.history.append({"role": "user", "content": user_message})
        messages = [system] + self.history[-MAX_HISTORY:]

        resp = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=2048,
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []
