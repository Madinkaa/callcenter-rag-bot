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
TOP_K         = 10
MAX_HISTORY   = 10
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

SYSTEM_PROMPT = """Ты — интеллектуальный ассистент колл-центра НПК. Твоя задача — отвечать на вопросы операторов, используя ТОЛЬКО предоставленный ниже контекст из базы знаний.

ВАЖНЫЕ ПРАВИЛА:
1. Всегда анализируй контекст ниже — в нём есть ответы на вопросы.
2. Если в контексте есть таблица или список — перечисли данные из неё. Не говори "информации нет", если в контексте есть строки/ячейки/пункты по теме.
3. Если контекст по теме найден, но неполный — дай то, что есть, и уточни что именно нужно дополнить.
4. Если контекст совсем пуст (написано "Информация не найдена") — ТОЛЬКО тогда скажи: "К сожалению, по этому вопросу информации в базе нет. Уточните у супервайзера."
5. Ты — виртуальный ИИ-помощник, НЕ живой оператор. НЕ называй своё имя, НЕ представляйся человеком и НЕ используй конструкции вроде "меня зовут...".

ФОРМАТ ОТВЕТА:
- Отвечай чётко и по делу, без лишних вступлений
- Если есть шаги или список участников/тарифов/услуг — перечисли их
- Если контекст содержит таблицу — перенеси данные из неё в понятный текст
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
            temperature=0.2,
            max_tokens=2048,
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []