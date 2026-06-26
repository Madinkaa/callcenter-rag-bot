import { Send } from 'lucide-react'
import { FormEvent, useState } from 'react'
import { useTranslation } from '../i18n/useTranslation'

interface Props {
  disabled?: boolean
  onSubmit: (text: string) => void
}

export function InputBar({ disabled, onSubmit }: Props) {
  const [value, setValue] = useState('')
  const { t } = useTranslation()

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
        placeholder={t('input.placeholder')}
        disabled={disabled}
      />
      <button className="send" type="submit" disabled={disabled || !value.trim()} aria-label={t('input.send')}>
        <Send size={16} />
      </button>
    </form>
  )
}
