import { Sparkles, Phone } from 'lucide-react'

export type TabKey = 'home' | 'contacts'

interface Props {
  active: TabKey
  onChange: (t: TabKey) => void
}

export function Tabs({ active, onChange }: Props) {
  const items = [
    { key: 'home' as TabKey, label: 'Главная', icon: <Sparkles size={18} /> },
    { key: 'contacts' as TabKey, label: 'Контакты', icon: <Phone size={18} /> },
  ]

  return (
    <div className="tabs" role="tablist">
      {items.map((it) => (
        <button
          key={it.key}
          className={'tab' + (active === it.key ? ' active' : '')}
          onClick={() => onChange(it.key)}
          role="tab"
          aria-selected={active === it.key}
        >
          {it.icon}
          <span>{it.label}</span>
        </button>
      ))}
    </div>
  )
}
