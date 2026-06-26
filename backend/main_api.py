"""
backend/main_api.py — FastAPI сервис для чат-бота колл-центра
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_agent import RAGAgent

app = FastAPI(title="CallCenter RAG Bot API")

# Разрешаем CORS для фронтенда на Vercel (и локально)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать точный домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Хранилище сессий (в памяти). Для production лучше Redis.
sessions: dict[str, RAGAgent] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    lang: str = "auto"   # ru | kz | en | auto


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"status": "ok", "service": "callcenter-rag-bot"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is empty")

    agent = sessions.setdefault(req.session_id, RAGAgent())
    try:
        answer = agent.chat(req.message, lang=req.lang)
    except Exception as e:
        err_detail = str(e)
        # Если лимит и Groq, и OpenAI исчерпан — возвращаем 429
        if "429" in err_detail or "rate_limit" in err_detail.lower() or "quota" in err_detail.lower():
            raise HTTPException(status_code=429, detail="Лимит API исчерпан. Попробуйте через несколько минут.")
        raise HTTPException(status_code=500, detail=err_detail)

    return ChatResponse(answer=answer)


@app.post("/reset")
def reset(session_id: str = "default"):
    if session_id in sessions:
        sessions[session_id].reset()
        return {"status": "reset", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}


@app.get("/health")
def health():
    return {"status": "healthy"}
