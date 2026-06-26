import { Sparkles, FileText, Phone } from 'lucide-react'
import { useTranslation } from '../i18n/useTranslation'

export type TabKey = 'home' | 'appeal' | 'contacts'

interface Props {
  active: TabKey
  onChange: (t: TabKey) => void
}

export function Tabs({ active, onChange }: Props) {
  const { t } = useTranslation()

  const items = [
    { key: 'home' as TabKey, label: t('tab.home'), icon: <Sparkles size={16} /> },
    { key: 'appeal' as TabKey, label: t('tab.appeal'), icon: <FileText size={16} /> },
    { key: 'contacts' as TabKey, label: t('tab.contacts'), icon: <Phone size={16} /> },
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
