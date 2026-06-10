import { Phone, Copy, Timer, Mail, Instagram, Linkedin, Send } from 'lucide-react'

export function ContactsTab() {
  const handleCopy = () => {
    navigator.clipboard?.writeText('+7 7272 97 91 00')
  }

  return (
    <div className="empty-screen contacts-screen">
      <div className="contacts-card">
        <div className="tag">ТЕЛЕФОН</div>
        <div className="big">+7 7272 97 91 00</div>
        <div className="sub">Звонок по тарифам вашего оператора</div>
        <a className="call-btn" href="tel:+77272979100">
          <Phone size={17} /> Позвонить
        </a>
        <button
          className="copy-btn"
          onClick={handleCopy}
          aria-label="Скопировать номер"
        >
          <Copy size={15} />
        </button>
      </div>

      <div className="schedule-card">
        <div className="head"><Timer size={14} /> Время работы</div>
        <div className="row">
          <div className="k">Понедельник – Пятница</div>
          <div className="v">8:40 – 17:40</div>
        </div>
        <div className="row">
          <div className="k">Суббота – Воскресенье</div>
          <div className="v">Выходной</div>
        </div>
      </div>

      <div className="contacts-card" style={{ background: '#fff', color: 'var(--text-primary)', border: '1px solid var(--border)' }}>
        <div className="tag" style={{ background: 'var(--primary-soft)', color: 'var(--primary)' }}>КОНТАКТЫ</div>
        <a className="row" href="mailto:info@npck.kz" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="k" style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Mail size={12} /> Email</div>
          <div className="v">info@npck.kz</div>
        </a>
        <a className="row" href="https://www.instagram.com/npck.kz/" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="k" style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Instagram size={12} /> Instagram</div>
          <div className="v">@npck.kz</div>
        </a>
        <a className="row" href="https://www.linkedin.com/company/npck/" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="k" style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Linkedin size={12} /> LinkedIn</div>
          <div className="v">npck</div>
        </a>
        <a className="row" href="https://t.me/npckkz" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="k" style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Send size={12} /> Telegram</div>
          <div className="v">@npckkz</div>
        </a>
      </div>
    </div>
  )
}
