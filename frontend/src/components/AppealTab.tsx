import {
  Download,
  Globe,
  ArrowRight,
  LogIn,
  ExternalLink,
  FileText,
  Phone,
} from 'lucide-react'

export function AppealTab() {
  return (
    <div className="appeal-page">
      {/* Шаг 1: Стать клиентом */}
      <div className="appeal-step">
        <div className="appeal-step-num">1</div>
        <div className="appeal-step-body">
          <div className="appeal-step-title">Стать клиентом</div>

          <a
            href="https://npck.kz/kak-stat-klientom-2/"
            target="_blank"
            rel="noopener noreferrer"
            className="appeal-link-card appeal-link-card--accent"
          >
            <div className="appeal-link-icon">
              <ExternalLink size={20} />
            </div>
            <div className="appeal-link-text">
              <div className="appeal-link-title">Инструкция по подключению</div>
              <div className="appeal-link-sub">На официальном сайте npck.kz</div>
            </div>
            <ArrowRight size={18} className="appeal-link-arrow" />
          </a>

          <div className="appeal-mini-card">
            <div className="appeal-mini-info">
              <div className="appeal-mini-icon">
                <FileText size={16} />
              </div>
              <div className="appeal-mini-text">
                <div className="appeal-mini-title">Шаблон заявления</div>
                <div className="appeal-mini-sub">.docx для новых клиентов</div>
              </div>
            </div>
            <a
              href="/Шаблон.docx?v=2"
              download="Шаблон_заявления_НПК.docx"
              className="appeal-mini-btn"
            >
              <Download size={14} />
              Скачать
            </a>
          </div>
        </div>
      </div>

      {/* Шаг 2: Подать обращение */}
      <div className="appeal-step">
        <div className="appeal-step-num">2</div>
        <div className="appeal-step-body">
          <div className="appeal-step-title">Подать обращение</div>

          <div className="appeal-option-card">
            <div className="appeal-option-header">
              <div className="appeal-option-icon existing">
                <LogIn size={18} />
              </div>
              <div className="appeal-option-label">Являюсь клиентом</div>
            </div>
            <p className="appeal-option-desc">
              Есть доступ к личному кабинету? Подайте заявку онлайн.
            </p>
            <div className="appeal-option-meta">
              <span>Быстрая подача</span>
              <span className="dot" />
              <span>Отслеживание статуса</span>
            </div>
            <a
              href="http://app.help-desk.kisc.kz/otrs/customer.pl?M=10&Actions=ServiceCatalogue&Param=%7B%22SearchString%22%3A%22%22%2C%22ServiceID%22%3A%22%22%2C%22TopService%22%3A%5B%222%22%2C%223%22%2C%224%22%2C%225%22%5D%2C%22ServiceIDTT%22%3A%22%22%7D"
              target="_blank"
              rel="noopener noreferrer"
              className="appeal-option-btn btn-gold"
            >
              <Globe size={14} />
              Личный кабинет
            </a>
          </div>
        </div>
      </div>

      {/* Подсказка */}
      <div className="appeal-bottom-hint">
        <Phone size={12} />
        <span>
          Нужна помощь? Звоните <strong>+7 727 297 91 00</strong>
        </span>
      </div>
    </div>
  )
}
