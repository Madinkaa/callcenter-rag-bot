"""
ingest.py — читает .docx файлы из папки docs/ и загружает в ChromaDB (локально).
Разбивает документы по логическим блокам (абзацам/секциям), а не механически.
"""

import os
import re
import uuid
from docx import Document
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

# ─── НАСТРОЙКИ ───────────────────────────────────────────────────────────────
DOCS_FOLDER   = "./docs"
COLLECTION    = "callcenter-docs"
CHROMA_FOLDER = "./chroma_db"
EMBED_MODEL   = "text-embedding-3-small"
MAX_CHUNK_LEN = 700    # максимум символов в одном чанке
MIN_CHUNK_LEN = 30     # минимум — иначе пропускаем
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def split_into_sections(text: str) -> list[str]:
    """
    Разбивает текст на логические блоки:
    1. Если есть маркеры Вопрос/Ответ — разбивает по ним
    2. Иначе — объединяет короткие абзацы с последующими длинными
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return []

    # Паттерн FAQ: строки начинающиеся с "Вопрос:" / "В.", "Ответ:" / "О."
    faq_pattern = re.compile(r'^(?:\d+\.?\s*)?(?:Вопрос|В\.|Ответ|О\.)\s*[:\-]?\s*', re.IGNORECASE)
    is_faq = any(faq_pattern.match(l) for l in lines)

    chunks = []
    current = []

    def flush():
        if current:
            joined = "\n".join(current).strip()
            if len(joined) >= MIN_CHUNK_LEN:
                if len(joined) > MAX_CHUNK_LEN:
                    joined = joined[:MAX_CHUNK_LEN]
                chunks.append(joined)
        return []

    if is_faq:
        # FAQ-режим: каждая пара Вопрос+Ответ = один чанк
        for line in lines:
            if faq_pattern.match(line):
                current = flush()
            current.append(line)
        flush()
    else:
        # Обычный режим: короткие строки (заголовки) присоединяем к следующей длинной
        buffer = []
        for line in lines:
            if len(line) < 60 and not line.endswith('.') and not line.endswith(';'):
                # Вероятно заголовок — сохраняем в буфер
                if buffer:
                    buffer = flush()
                buffer.append(line)
            else:
                if buffer:
                    buffer.append(line)
                    joined = "\n".join(buffer).strip()
                    if len(joined) >= MIN_CHUNK_LEN:
                        if len(joined) > MAX_CHUNK_LEN:
                            joined = joined[:MAX_CHUNK_LEN]
                        chunks.append(joined)
                    buffer = []
                else:
                    current.append(line)
                    if sum(len(c) for c in current) >= MAX_CHUNK_LEN:
                        current = flush()
        if buffer:
            joined = "\n".join(buffer).strip()
            if len(joined) >= MIN_CHUNK_LEN:
                if len(joined) > MAX_CHUNK_LEN:
                    joined = joined[:MAX_CHUNK_LEN]
                chunks.append(joined)
        if current:
            flush()

    return chunks


def get_embedding(text: str) -> list[float]:
    # OpenAI лимит ~8192 токенов ≈ 24000 символов кириллицы
    if len(text) > 15000:
        text = text[:15000]
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


def main():
    docx_files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".docx") and not f.startswith("~")]
    if not docx_files:
        print("[!] Нет .docx файлов в папке docs/")
        return

    print(f"[INFO] Найдено файлов: {len(docx_files)}")

    # Удаляем старую коллекцию
    try:
        chroma_client.delete_collection(COLLECTION)
        print(f"[OK] Старая коллекция удалена.")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"[OK] Коллекция '{COLLECTION}' создана.")

    all_ids = []
    all_embeddings = []
    all_documents = []
    all_metadatas = []

    for filename in docx_files:
        filepath = os.path.join(DOCS_FOLDER, filename)
        print(f"  Читаю: {filename}")
        text = read_docx(filepath)
        chunks = split_into_sections(text)
        print(f"    -> {len(chunks)} логических блоков")

        for chunk in chunks:
            emb = get_embedding(chunk)
            all_ids.append(str(uuid.uuid4()))
            all_embeddings.append(emb)
            all_documents.append(chunk)
            all_metadatas.append({"source": filename})

    # Загружаем пакетами
    batch_size = 100
    for i in range(0, len(all_ids), batch_size):
        collection.add(
            ids=all_ids[i:i+batch_size],
            embeddings=all_embeddings[i:i+batch_size],
            documents=all_documents[i:i+batch_size],
            metadatas=all_metadatas[i:i+batch_size],
        )
        print(f"  [INFO] Загружено {min(i+batch_size, len(all_ids))}/{len(all_ids)} блоков...")

    print(f"\n[DONE] Готово! Загружено {len(all_ids)} блоков в ChromaDB.")
    print("Теперь скопируй папку chroma_db/ в backend/chroma_db/ и redeploy.")


if __name__ == "__main__":
    main()
