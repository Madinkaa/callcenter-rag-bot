import { X, RotateCcw } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { useTranslation } from '../i18n/useTranslation'

interface Props {
  title: string
  status: string
  onClose: () => void
  onReset?: () => void
}

export function Header({ title, status, onClose, onReset }: Props) {
  const { lang, setLang } = useI18n()
  const { t } = useTranslation()

  return (
    <div className="header">
      <img src="/npck-logo.png" className="header-logo" alt={t('header.logoAlt')} />
      <div className="header-grow">
        <div className="title">{title}</div>
        <div className="sub">
          <div className="dot" />
          {status}
        </div>
      </div>

      <div className="lang-switcher">
        {(['ru', 'kz', 'en'] as const).map((l) => (
          <button
            key={l}
            className={`lang-btn ${lang === l ? 'active' : ''}`}
            onClick={() => setLang(l)}
            aria-label={l}
          >
            {t(`lang.${l}`)}
          </button>
        ))}
      </div>

      {onReset && (
        <button className="header-action" onClick={onReset} aria-label={t('header.reset')} title={t('header.reset')}>
          <RotateCcw size={16} />
        </button>
      )}
      <button className="header-close" onClick={onClose} aria-label={t('header.close')}>
        <X size={16} />
      </button>
    </div>
  )
}
