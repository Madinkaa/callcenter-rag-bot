"""
rag_agent.py — RAG агент для колл-центра (ChromaDB локально)
"""

import os
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

SYSTEM_PROMPT = """Ты — интеллектуальный ассистент колл-центра. Твоя задача — помогать операторам быстро находить точную информацию из базы знаний и следовать скриптам.

ПОВЕДЕНИЕ:
- Отвечай ТОЛЬКО на основе предоставленного контекста из базы знаний
- Если информации недостаточно или вопрос расплывчатый — задай ОДИН уточняющий вопрос
- Если в базе есть готовый скрипт по теме — следуй его структуре
- Если информации нет совсем — скажи: "К сожалению, по этому вопросу информации в базе нет. Уточните у супервайзера."

УТОЧНЯЮЩИЕ ВОПРОСЫ (примеры когда задавать):
- "подключить услугу" → "Подскажите, какую именно услугу вы хотите подключить? Я найду точную инструкцию."
- "проблема с тарифом" → "Уточните, пожалуйста, что именно за проблема — списание, смена тарифа или что-то другое?"
- "не работает" → "Что именно не работает? Опишите проблему подробнее."

ФОРМАТ ОТВЕТА:
- Отвечай чётко и по делу, без лишних вступлений
- Если есть шаги — нумеруй их
- Тон: вежливый, профессиональный

КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ:
{context}"""


def get_embedding(text: str) -> list[float]:
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


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
    return "\n\n---\n\n".join(parts) if parts else "Информация не найдена в базе знаний."


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
            temperature=0.3,
            max_tokens=1024,
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []