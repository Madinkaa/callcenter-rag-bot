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
        answer = agent.chat(req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
