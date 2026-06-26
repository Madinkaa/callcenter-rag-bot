import { Sparkles, FileText, Phone } from 'lucide-react'

export type TabKey = 'home' | 'appeal' | 'contacts'

interface Props {
  active: TabKey
  onChange: (t: TabKey) => void
}

export function Tabs({ active, onChange }: Props) {
  const items = [
    { key: 'home' as TabKey, label: 'Главная', icon: <Sparkles size={16} /> },
    { key: 'appeal' as TabKey, label: 'Подать обращение', icon: <FileText size={16} /> },
    { key: 'contacts' as TabKey, label: 'Контакты АО НПК', icon: <Phone size={16} /> },
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
