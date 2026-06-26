import {
  Download,
  Globe,
  ExternalLink,
  UserPlus,
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

          <div className="appeal-option-card">
            <div className="appeal-option-header">
              <div className="appeal-option-icon new">
                <UserPlus size={18} />
              </div>
              <div className="appeal-option-label">Стать клиентом</div>
            </div>
            <p className="appeal-option-desc">
              Нет личного кабинета? Ознакомьтесь с инструкцией по подключению и скачайте шаблон заявления.
            </p>
            <div className="appeal-option-meta">
              <span>support@npck.kz</span>
            </div>
            <div className="appeal-option-actions">
              <a
                href="https://npck.kz/kak-stat-klientom-2/"
                target="_blank"
                rel="noopener noreferrer"
                className="appeal-option-btn btn-green"
              >
                <ExternalLink size={14} />
                Инструкция
              </a>
              <a
                href="/Шаблон.docx?v=2"
                download="Шаблон_заявления_НПК.docx"
                className="appeal-option-btn btn-green-outline"
              >
                <Download size={14} />
                Шаблон
              </a>
            </div>
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
                <img src="/icons8-client-64.png" alt="Клиент" className="appeal-option-img" />
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
