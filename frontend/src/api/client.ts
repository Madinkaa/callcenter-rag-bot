import axios from 'axios'

const BASE = (import.meta.env?.VITE_API_BASE as string | undefined) || 'http://localhost:8000'

export const api = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
})

export interface ChatRequest {
  message: string
  session_id: string
}

export interface ChatResponse {
  answer: string
}

export async function sendMessage(sessionId: string, message: string): Promise<string> {
  const { data } = await api.post<ChatResponse>('/chat', { session_id: sessionId, message })
  return data.answer
}

export async function resetSession(sessionId: string): Promise<void> {
  await api.post('/reset', {}, { params: { session_id: sessionId } })
}

export async function healthCheck(): Promise<boolean> {
  try {
    const { data } = await api.get('/health')
    return data?.status === 'healthy'
  } catch {
    return false
  }
}
