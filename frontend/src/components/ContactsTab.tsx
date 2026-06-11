import {
  Phone,
  Timer,
  Mail,
  Instagram,
  Linkedin,
  Send,
  MapPin,
  ExternalLink,
} from 'lucide-react'

export function ContactsTab() {
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
        <div className="contacts-avatar">Н</div>
        <h3>Связаться с нами</h3>
        <p>Мы всегда на связи и готовы помочь</p>
      </div>

      {/* Телефон */}
      <div className="contacts-phone-card">
        <div className="phone-ring">
          <div className="phone-ring-inner">
            <Phone size={24} />
          </div>
        </div>
        <div className="phone-badge">Телефон колл-центра</div>
        <div className="phone-number">+7 7272 97 91 00</div>
        <div className="phone-divider" />
        <div className="phone-sub">Звонок по тарифам вашего оператора</div>
        <a href="tel:+77272979100" className="phone-call-btn">
          <Phone size={16} /> Позвонить сейчас
        </a>
      </div>

      {/* Время работы */}
      <div className="contacts-schedule">
        <div className="schedule-title">
          <Timer size={14} />
          <span>Время работы</span>
        </div>
        <div className="schedule-row">
          <span className="day">Пн – Пт</span>
          <span className="time">8:40 – 17:40</span>
        </div>
        <div className="schedule-row">
          <span className="day">Сб – Вс</span>
          <span className="time off">Выходной</span>
        </div>
      </div>

      {/* Соцсети */}
      <div className="contacts-socials">
        <div className="socials-title">Мы в социальных сетях</div>
        <div className="socials-grid">
          {socials.map((s) => (
            <a
              key={s.label}
              href={s.href}
              target="_blank"
              rel="noopener noreferrer"
              className="social-card"
              style={{ '--social-color': s.color } as React.CSSProperties}
            >
              <div className="social-icon">{s.icon}</div>
              <div className="social-info">
                <div className="social-label">{s.label}</div>
                <div className="social-value">{s.value}</div>
              </div>
              <ExternalLink size={14} className="social-arrow" />
            </a>
          ))}
        </div>
      </div>

      {/* Адрес */}
      <div className="contacts-address">
        <MapPin size={14} />
        <span>г. Алматы, Микрорайон Коктем-3, 21</span>
      </div>
    </div>
  )
}
