import {
  Phone,
  Timer,
  Mail,
  Instagram,
  Linkedin,
  Send,
  MapPin,
} from 'lucide-react'
import { useTranslation } from '../i18n/useTranslation'

export function ContactsTab() {
  const { t } = useTranslation()

  const socials = [
    {
      icon: <Mail size={18} />,
      label: 'Email',
      value: 'support@npck.kz',
      href: 'mailto:support@npck.kz',
      color: '#EA4335',
    },
    {
      icon: <Send size={18} />,
      label: 'Telegram',
      value: '@npckkz',
      href: 'https://t.me/npckkz',
      color: '#0088cc',
    },
    {
      icon: <Instagram size={18} />,
      label: 'Instagram',
      value: '@npck.kz',
      href: 'https://www.instagram.com/npck.kz/',
      color: '#E4405F',
    },
    {
      icon: <Linkedin size={18} />,
      label: 'LinkedIn',
      value: 'npck',
      href: 'https://www.linkedin.com/company/npck/',
      color: '#0A66C2',
    },
  ]

  return (
    <div className="contacts-wrapper">
      {/* Заголовок */}
      <div className="contacts-hero">
        <img className="contacts-avatar" src="/npck-avatar.png" alt="НПК" />
        <p>{t('contacts.heroText')}</p>
      </div>

      {/* Телефон */}
      <div className="contacts-phone-card">
        <div className="phone-ring">
          <div className="phone-wave" />
          <div className="phone-ring-inner">
            <Phone size={24} />
          </div>
        </div>
        <div className="phone-badge">{t('contacts.phoneBadge')}</div>
        <div className="phone-number">+7 727 297 91 00</div>
        <div className="phone-divider" />
        <div className="phone-sub">{t('contacts.phoneSub')}</div>
        <a href="tel:+77272979100" className="phone-call-btn">
          <Phone size={16} /> {t('contacts.callNow')}
        </a>
      </div>

      {/* Время работы */}
      <div className="contacts-schedule">
        <div className="schedule-title">
          <Timer size={14} />
          <span>{t('contacts.scheduleTitle')}</span>
        </div>
        <div className="schedule-row">
          <span className="day">{t('contacts.dayWeek')}</span>
          <span className="time">{t('contacts.timeWeek')}</span>
        </div>
        <div className="schedule-row">
          <span className="day">{t('contacts.dayWeekend')}</span>
          <span className="time off">{t('contacts.timeWeekend')}</span>
        </div>
      </div>

      {/* Соцсети */}
      <div className="contacts-socials">
        <div className="socials-title">{t('contacts.socialsTitle')}</div>
        <div className="socials-row">
          {socials.map((s) => (
            <a
              key={s.label}
              href={s.href}
              target="_blank"
              rel="noopener noreferrer"
              className="social-chip"
              title={`${s.label}: ${s.value}`}
              style={{ '--social-color': s.color } as React.CSSProperties}
            >
              <span className="social-chip-icon">{s.icon}</span>
              <span className="social-chip-label">{s.label}</span>
            </a>
          ))}
        </div>
      </div>

      {/* Адрес */}
      <div className="contacts-address">
        <MapPin size={14} />
        <span>{t('contacts.address')}</span>
      </div>
    </div>
  )
}
