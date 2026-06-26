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
TOP_K         = 8
MAX_HISTORY   = 10
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection    = chroma_client.get_collection(name=COLLECTION)

SPECIFIC_SYSTEMS = {
    "цоид", "спбс", "собс", "фасти", "смэп", "смк",
    "мспд", "мсмп", "цифровой тенге", "антифрод", "нац клиринг",
    "удостоверяющий центр", "уц нпк", "национальная платёжная",
}

VAGUE_KEYWORDS = {
    "подключить", "услуга", "услуги", "подключение",
    "тариф", "тарифы", "стоимость", "цена", "сколько стоит",
    "проблема", "не работает", "ошибка", "сбой",
    "как", "что", "где", "когда", "зачем",
}

VAGUE_QUESTION = "Подскажите, пожалуйста, что именно вас интересует? Например, подключение к ЦОИД, СПБС, СОБС, Антифрод-центру, или может, тарифы на конкретную услугу?"

KAZAKH_CHARS = set("әіңғүұқөһ")


def detect_language(text: str) -> str:
    """Определяет язык текста: ru | kz | en."""
    text_lower = text.lower()
    if any(ch in text_lower for ch in KAZAKH_CHARS):
        return "kz"
    # Проверяем на кириллицу (без казахских = русский)
    if any("а" <= ch <= "я" or ch in "ёқәіңғүұөһ" for ch in text_lower):
        return "ru"
    return "en"


LANGUAGE_RULES = {
    "ru": "Отвечай строго на русском языке.",
    "kz": "Жауап беруді тек қазақ тілінде жүргіз.",
    "en": "Answer strictly in English.",
}

SYSTEM_PROMPT = """Ты — интеллектуальный ИИ-ассистент колл-центра НПК.

{lang_rule}

Твоя задача — анализировать предоставленный ниже контекст и давать точный ответ ПО ТЕМЕ вопроса.

ЖЁСТКИЕ ПРАВИЛА (не нарушай):
1. ВНИМАТЕЛЬНО прочитай контекст. Если в нём есть строки, вопросы, ответы, таблицы или списки, ОТНОСЯЩИЕСЯ к теме вопроса — ИСПОЛЬЗУЙ их для ответа.
2. Если контекст содержит FAQ (вопрос-ответ) по теме — ответь данными из FAQ.
3. Если контекст содержит таблицу — перенеси данные из таблицы в текст.
4. Если контекст есть, но неполный — дай то, что есть, и уточни, что можно добавить.
5. Если контекст полностью пуст (написано "Информация не найдена") — ТОЛЬКО тогда скажи: "К сожалению, по этому вопросу информации в базе нет. Уточните у супервайзера."
6. Ты — виртуальный ИИ-помощник. НЕ называй своё имя. НЕ представляйся человеком.
7. Если в контексте указаны устаревшие контакты — используй АКТУАЛЬНЫЕ контакты из раздела ниже.
8. Если контекст содержит определение аббревиатуры или термина — используй ТОЛЬКО его. НЕ придумывай свои расшифровки аббревиатур и НЕ используй общие знания, отсутствующие в контексте.

АКТУАЛЬНЫЕ КОНТАКТЫ НПК (всегда используй только их):
- Телефон колл-центра: +7 7272 97 91 00
- Email: support@npck.kz
- Портал управления: https://cms.npck.kz/
- Официальный сайт: https://npck.kz

ФОРМАТ:
- Без вступлений, сразу по делу.
- Если есть шаги — нумеруй.
- Тон: вежливый, профессиональный.

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
    """Проверяет, является ли вопрос слишком расплывчатым."""
    q_lower = query.lower().strip()
    # Если в вопросе есть конкретная система — это НЕ расплывчатый вопрос
    if any(sys in q_lower for sys in SPECIFIC_SYSTEMS):
        return False
    words = set(q_lower.split())
    # Короткие вопросы с общими словами и без конкретики — расплывчатые
    if len(words) <= 3 and any(w in VAGUE_KEYWORDS for w in words):
        return True
    if len(q_lower.split()) <= 2:
        return True
    return False


def sanitize_answer(answer: str) -> str:
    """Заменяет устаревшие контакты в ответе бота на актуальные."""
    replacements = [
        # URL
        ("sms.npck.kz", "cms.npck.kz"),
        # Email: любые osis-варианты → единый support@npck.kz
        ("support-support-osis@npck.kz", "support@npck.kz"),
        ("support-osis@npck.kz", "support@npck.kz"),
        ("osis@npck.kz", "support@npck.kz"),
        ("info@npck.kz", "support@npck.kz"),
        # Phone
        ("8 (727) 250-66-75", "+7 7272 97 91 00"),
        ("8(727)250-66-75", "+7 7272 97 91 00"),
        ("+7 (727) 250-66-75", "+7 7272 97 91 00"),
    ]
    for old, new in replacements:
        answer = answer.replace(old, new)
        answer = answer.replace(old.upper(), new)
        answer = answer.replace(old.title(), new)
    return answer


class RAGAgent:
    def __init__(self):
        self.history: list[dict] = []

    def chat(self, user_message: str, lang: str = "auto") -> str:
        # Определяем язык
        detected = detect_language(user_message) if lang == "auto" else lang
        lang_rule = LANGUAGE_RULES.get(detected, LANGUAGE_RULES["ru"])

        # ── ШАГ 1: Если вопрос расплывчатый — сразу уточняем, НЕ вызывая LLM ──
        if is_vague(user_message):
            self.history.append({"role": "user", "content": user_message})
            # Переводим уточняющий вопрос на язык пользователя
            vague_translations = {
                "kz": "Өтінемін, нақты не қызықтырады? Мысалы, ЦОИД, СПБС, СОБС, Антифрод-орталыққа қосылу немесе нақты қызметтің тарифі.",
                "en": "Please tell me what exactly you are interested in? For example, connecting to COID, SPBS, SOBS, Anti-Fraud Center, or tariffs for a specific service.",
            }
            answer = vague_translations.get(detected, VAGUE_QUESTION)
            self.history.append({"role": "assistant", "content": answer})
            return answer

        # ── ШАГ 2: Если вопрос короткий — добавляем контекст из предыдущего ответа ──
        search_query = user_message
        if len(user_message.split()) <= 5 and self.history:
            last_bot = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"),
                ""
            )
            # Не подмешиваем прошлый ответ, если он был ошибкой/уточнением/слишком коротким
            bad_phrases = ["информации в базе нет", "уточните", "подскажите, пожалуйста"]
            if not any(bp in last_bot.lower() for bp in bad_phrases) and len(last_bot) > 80:
                search_query = f"{last_bot[:300]} {user_message}"

        # ── ШАГ 3: Ищем контекст и вызываем LLM ──
        context = search(search_query)
        system = {
            "role": "system",
            "content": SYSTEM_PROMPT.format(context=context, lang_rule=lang_rule),
        }
        self.history.append({"role": "user", "content": user_message})
        messages = [system] + self.history[-MAX_HISTORY:]

        # Сначала пробуем Groq, если лимит исчерпан — fallback на OpenAI
        try:
            resp = groq_client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=2048,
            )
            answer = resp.choices[0].message.content
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate_limit" in err_str.lower():
                # Fallback на OpenAI gpt-4o-mini
                resp = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.2,
                    max_tokens=2048,
                )
                answer = resp.choices[0].message.content
            else:
                raise

        answer = sanitize_answer(answer)
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.history = []
