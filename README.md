# 🤖 Чат-бот колл-центра (RAG)

Простое RAG-приложение для операторов колл-центра: задаёшь вопрос — бот ищет в базе знаний и отвечает.

## Архитектура

| Компонент | Технология | Деплой |
|-----------|-----------|--------|
| Бэкенд | FastAPI + ChromaDB | Railway |
| Фронтенд | HTML/CSS/JS | Vercel |
| LLM | Groq (llama-3.3-70b) | — |
| Embeddings | OpenAI (text-embedding-3-small) | — |

---

## 📁 Структура проекта

```
call_center_file/
├── backend/
│   ├── main_api.py          # FastAPI приложение
│   ├── rag_agent.py         # RAG логика
│   ├── chroma_db/           # Локальная база ChromaDB
│   ├── requirements.txt
│   └── Procfile             # Railway: команда запуска
├── frontend/
│   ├── index.html           # Чат-интерфейс
│   └── vercel.json          # Vercel конфиг
├── docs/                    # Исходные документы (PDF/DOCX)
├── ingest.py                # Скрипт для загрузки документов в ChromaDB
└── README.md
```

---

## 🚀 Деплой

### 1. Бэкенд → Railway

1. Установи Railway CLI (опционально) или используй веб-интерфейс: https://railway.app
2. Создай новый проект
3. Загрузи папку `backend/` (или подключи GitHub репозиторий)
4. Добавь переменные окружения в Railway Dashboard → Variables:
   - `OPENAI_API_KEY` — ключ от OpenAI
   - `GROQ_API_KEY` — ключ от Groq
5. Railway сам найдёт `Procfile` и запустит: `uvicorn main_api:app --host 0.0.0.0 --port $PORT`
6. Получи публичный URL (например, `https://callcenter-bot-production.up.railway.app`)

> ⚠️ **Важно**: ChromaDB (`chroma_db/`) уже внутри `backend/`, поэтому база уедет на Railway вместе с кодом.

### 2. Фронтенд → Vercel

1. Зайди на https://vercel.com
2. Импортируй проект (или папку `frontend/`)
3. Vercel сам определит `vercel.json` и задеплоит статику
4. Получи URL: `https://callcenter-bot.vercel.app`

### 3. Подключи фронт к бэку

Открой `frontend/index.html` и замени переменную `API_BASE`:

```javascript
// В начале index.html
const API_BASE = "https://callcenter-bot-production.up.railway.app";
```

Закоммить изменение и redeploy на Vercel.

---

## 🧪 Локальный запуск

### Бэкенд

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main_api:app --reload --port 8000
```

Открой http://127.0.0.1:8000/docs — интерактивная документация API.

### Фронтенд

Просто открой `frontend/index.html` в браузере или запусти локальный сервер:

```bash
cd frontend
python -m http.server 3000
```

При локальном тесте в `index.html` оставь:
```javascript
const API_BASE = "http://127.0.0.1:8000";
```

---

## 🔌 API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Проверка статуса |
| GET | `/health` | Healthcheck |
| POST | `/chat` | Отправить сообщение |
| POST | `/reset` | Сбросить диалог |

**Пример запроса:**
```bash
curl -X POST https://<railway-url>/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Как подключить услугу?", "session_id": "demo"}'
```

---

## 🔑 Переменные окружения

| Переменная | Где берётся |
|------------|-------------|
| `OPENAI_API_KEY` | https://platform.openai.com |
| `GROQ_API_KEY` | https://console.groq.com |

---

## 📝 Как обновить базу знаний

1. Положи новые документы в `docs/`
2. Запусти `ingest.py` (из корня проекта):
   ```bash
   python ingest.py
   ```
3. Скопируй обновлённую `chroma_db/` в `backend/chroma_db/`
4. Перезалей бэкенд на Railway

---

## 💡 Доработки на будущее

- Добавить Redis для хранения сессий (сейчас в памяти)
- Авторизация по токену
- Интерфейс загрузки документов прямо из чата
- Rate limiting на API
