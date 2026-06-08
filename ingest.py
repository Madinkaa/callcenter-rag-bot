"""
ingest.py — читает .docx файлы из папки docs/ и загружает в ChromaDB (локально)
Запусти ОДИН РАЗ перед первым использованием чат-бота.
"""

import os
import uuid
from docx import Document
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

# ─── НАСТРОЙКИ ───────────────────────────────────────────────────────────────
DOCS_FOLDER   = "./docs"
COLLECTION    = "callcenter-docs"
CHROMA_FOLDER = "./chroma_db"   # папка где хранится база локально
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 100
EMBED_MODEL   = "text-embedding-3-small"
# ─────────────────────────────────────────────────────────────────────────────

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_FOLDER)


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c.strip()]


def get_embedding(text: str) -> list[float]:
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding


def main():
    docx_files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".docx")]
    if not docx_files:
        print("[!] Нет .docx файлов в папке docs/")
        return

    print(f"[→] Найдено файлов: {len(docx_files)}")

    # Удаляем старую коллекцию если есть, создаём новую
    try:
        chroma_client.delete_collection(COLLECTION)
        print(f"[✓] Старая коллекция удалена.")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"[✓] Коллекция '{COLLECTION}' создана.")

    all_ids = []
    all_embeddings = []
    all_documents = []
    all_metadatas = []

    for filename in docx_files:
        filepath = os.path.join(DOCS_FOLDER, filename)
        print(f"  Читаю: {filename}")
        text = read_docx(filepath)
        chunks = chunk_text(text)
        print(f"    → {len(chunks)} чанков")

        for chunk in chunks:
            emb = get_embedding(chunk)
            all_ids.append(str(uuid.uuid4()))
            all_embeddings.append(emb)
            all_documents.append(chunk)
            all_metadatas.append({"source": filename})

    # Загружаем пакетами по 100
    batch_size = 100
    for i in range(0, len(all_ids), batch_size):
        collection.add(
            ids=all_ids[i:i+batch_size],
            embeddings=all_embeddings[i:i+batch_size],
            documents=all_documents[i:i+batch_size],
            metadatas=all_metadatas[i:i+batch_size],
        )
        print(f"  [→] Загружено {min(i+batch_size, len(all_ids))}/{len(all_ids)} чанков...")

    print(f"\n✅ Готово! Загружено {len(all_ids)} чанков в ChromaDB.")
    print("Теперь запускай: python main.py")


if __name__ == "__main__":
    main()
