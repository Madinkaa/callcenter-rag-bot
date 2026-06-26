import { useEffect, useRef, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import axios from 'axios'
import { Header } from './Header'
import { Bubble, TypingBubble } from './Bubble'
import { InputBar } from './InputBar'
import { Tabs, TabKey } from './Tabs'
import { ContactsTab } from './ContactsTab'
import { AppealTab } from './AppealTab'
import { sendMessage, resetSession } from '../api/client'

interface Msg {
  id: string
  sender: 'user' | 'ai'
  content: string
  ts: number
}

const STORAGE_KEY = 'npck_ai_session_v1'

function loadSession(): { sessionId: string; messages: Msg[] } | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function saveSession(sessionId: string, messages: Msg[]) {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ sessionId, messages }))
}

export function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [tab, setTab] = useState<TabKey>('home')
  const [sessionId, setSessionId] = useState<string>('')
  const [messages, setMessages] = useState<Msg[]>([])
  const [thinking, setThinking] = useState(false)
  const bodyRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const saved = loadSession()
    if (saved) {
      setSessionId(saved.sessionId)
      setMessages(saved.messages)
    } else {
      const id = crypto.randomUUID()
      setSessionId(id)
      setMessages([])
      saveSession(id, [])
    }
  }, [])

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight
    }
  }, [messages.length, thinking])

  const handleSend = async (text: string) => {
    if (!sessionId) return
    const userMsg: Msg = { id: crypto.randomUUID(), sender: 'user', content: text, ts: Date.now() }
    const nextMessages = [...messages, userMsg]
    setMessages(nextMessages)
    saveSession(sessionId, nextMessages)
    setThinking(true)

    try {
      const answer = await sendMessage(sessionId, text)
      const aiMsg: Msg = { id: crypto.randomUUID(), sender: 'ai', content: answer, ts: Date.now() }
      const finalMessages = [...nextMessages, aiMsg]
      setMessages(finalMessages)
      saveSession(sessionId, finalMessages)
    } catch (err: any) {
      let content = 'Не удалось связаться с сервером. Попробуйте позже.'
      if (axios.isAxiosError(err)) {
        if (err.code === 'ECONNABORTED' || err.code === 'ETIMEDOUT') {
          content = 'Сервер долго не отвечает (возможно, просыпается после простоя). Попробуйте ещё раз через 30 секунд.'
        } else if (err.response?.status === 502 || err.response?.status === 503) {
          content = 'Сервис временно недоступен. Попробуйте через минуту.'
        } else if (err.response?.status === 429) {
          content = 'Лимит запросов к ИИ исчерпан. Попробуйте через несколько минут.'
        } else if (err.response?.status === 500) {
          content = 'Ошибка на сервере при обработке запроса. Попробуйте позже.'
        } else if (!err.response) {
          content = 'Нет соединения с сервером. Проверьте интернет или попробуйте позже.'
        }
      }
      const errMsg: Msg = {
        id: crypto.randomUUID(),
        sender: 'ai',
        content,
        ts: Date.now(),
      }
      const finalMessages = [...nextMessages, errMsg]
      setMessages(finalMessages)
      saveSession(sessionId, finalMessages)
    } finally {
      setThinking(false)
    }
  }

  const handleReset = () => {
    if (!sessionId) return
    resetSession(sessionId).catch(() => {})
    const id = crypto.randomUUID()
    setSessionId(id)
    setMessages([])
    saveSession(id, [])
  }

  const headerTitle =
    tab === 'home' ? 'Контакт-центр НПК' :
    tab === 'appeal' ? 'Подать обращение' :
    'Контакты НПК'

  const headerStatus =
    tab === 'home' ? 'Онлайн' :
    tab === 'appeal' ? 'Служба поддержки' :
    'Колл-центр'

  if (!open) {
    return (
      <div className="npck-page">
        <button className="fab" onClick={() => setOpen(true)} aria-label="Открыть чат">
          <MessageSquare size={24} />
        </button>
      </div>
    )
  }

  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour >= 5 && hour < 12) {
      return 'Доброе утро! Я — ИИ-помощник НПК. Задайте вопрос — найду ответ в базе знаний.'
    }
    if (hour >= 12 && hour < 18) {
      return 'Добрый день! Я — ИИ-помощник НПК. Задайте вопрос — найду ответ в базе знаний.'
    }
    return 'Добрый вечер! Я — ИИ-помощник НПК. Задайте вопрос — найду ответ в базе знаний.'
  }

  return (
    <div className="npck-page">
      <div className="widget">
        <Header
          title={headerTitle}
          status={headerStatus}
          onClose={() => setOpen(false)}
          onReset={tab === 'home' ? handleReset : undefined}
        />
        {tab === 'home' && (
          <>
            <div className="body" ref={bodyRef}>
              {messages.length === 0 && (
                <Bubble
                  sender="ai"
                  content={getGreeting()}
                />
              )}
              {messages.map((m) => (
                <Bubble key={m.id} sender={m.sender} content={m.content} time={m.ts} />
              ))}
              {thinking && <TypingBubble />}
            </div>
            <InputBar onSubmit={handleSend} disabled={thinking} />
          </>
        )}
        {tab === 'appeal' && <AppealTab />}
        {tab === 'contacts' && <ContactsTab />}
        <Tabs active={tab} onChange={setTab} />
      </div>
    </div>
  )
}
