import { Send } from 'lucide-react'
import { FormEvent, useState } from 'react'

interface Props {
  disabled?: boolean
  onSubmit: (text: string) => void
}

export function InputBar({ disabled, onSubmit }: Props) {
  const [value, setValue] = useState('')

  const submit = (e: FormEvent) => {
    e.preventDefault()
    const v = value.trim()
    if (!v || disabled) return
    onSubmit(v)
    setValue('')
  }

  return (
    <form className="input-bar" onSubmit={submit}>
      <input
        className="field"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Введите сообщение..."
        disabled={disabled}
      />
      <button className="send" type="submit" disabled={disabled || !value.trim()} aria-label="Отправить">
        <Send size={16} />
      </button>
    </form>
  )
}
