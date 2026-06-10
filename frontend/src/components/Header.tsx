import { X, RotateCcw } from 'lucide-react'

interface Props {
  title: string
  status: string
  onClose: () => void
  onReset?: () => void
}

export function Header({ title, status, onClose, onReset }: Props) {
  return (
    <div className="header">
      <div className="avatar">Н</div>
      <div className="header-grow">
        <div className="title">{title}</div>
        <div className="sub">
          <div className="dot" />
          {status}
        </div>
      </div>
      {onReset && (
        <button className="header-action" onClick={onReset} aria-label="Сбросить диалог" title="Сбросить">
          <RotateCcw size={16} />
        </button>
      )}
      <button className="header-close" onClick={onClose} aria-label="Закрыть">
        <X size={16} />
      </button>
    </div>
  )
}
