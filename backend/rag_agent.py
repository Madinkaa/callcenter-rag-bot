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
TOP_K         = 3
MAX_HISTORY   = 3
MAX_CONTEXT   = 2500
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

SYSTEM_PROMPT = """Ты — ассистент НПК (Национальная Корпорация Платежей). Отвечай операторам колл-центра ТОЛЬКО на основе предоставленного контекста из базы знаний.

ПРАВИЛА:
- Если в контексте есть прямой ответ — приведи его дословно или кратко перефразируй
- Если информации недостаточно — задай ОДИН уточняющий вопрос
- Если в контексте есть скрипт — следуй его структуре
- Не выдумывай ничего за пределами контекста
- Тон: вежливый, профессиональный

КОНТЕКСТ:
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
        parts.append(f"[{i}] {source}\n{doc}")
    return "\n\n---\n\n".join(parts) if parts else ""


class RAGAgent:
    def __init__(self):
        self.history: list[dict] = []

    def chat(self, user_message: str) -> str:
        # Короткий вопрос — добавляем контекст из истории
        search_query = user_message
        if len(user_message.split()) <= 6 and self.history:
            last_user = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "user"), ""
            )
            last_bot = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"), ""
            )
            search_query = f"{last_user} {last_bot[:150]} {user_message}"

        context = search(search_query)
        # Строго ограничиваем контекст для Groq TPM
        if len(context) > MAX_CONTEXT:
            context = context[:MAX_CONTEXT] + "\n[...]"

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
