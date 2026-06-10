interface Props {
  sender: 'user' | 'ai'
  content: string
  time?: string | number
}

function fmt(ts?: number | string): string | undefined {
  if (!ts) return undefined
  try {
    const d = typeof ts === 'number' ? new Date(ts) : new Date(ts)
    return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return undefined
  }
}

export function Bubble({ sender, content, time }: Props) {
  if (sender === 'user') {
    return (
      <div className="bubble user">
        <div className="msg">
          <div>{content}</div>
          {time && <div className="time">{fmt(time)}</div>}
        </div>
      </div>
    )
  }

  return (
    <div className="bubble">
      <div className="av">Н</div>
      <div className="inner">
        <div className="accent" />
        <div className="msg">
          <div>{content}</div>
          {time && <div className="time">{fmt(time)}</div>}
        </div>
      </div>
    </div>
  )
}

export function TypingBubble() {
  return (
    <div className="bubble">
      <div className="av">Н</div>
      <div className="inner">
        <div className="accent" />
        <div className="typing">
          <div className="dot" />
          <div className="dot" />
          <div className="dot" />
        </div>
      </div>
    </div>
  )
}
