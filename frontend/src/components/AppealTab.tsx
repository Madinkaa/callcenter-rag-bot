import {
  Download,
  Globe,
  ExternalLink,
  UserPlus,
  Phone,
} from 'lucide-react'
import { useTranslation } from '../i18n/useTranslation'
import { useI18n } from '../i18n/I18nContext'

export function AppealTab() {
  const { t } = useTranslation()
  const { lang } = useI18n()

  const instructionUrl =
    lang === 'kz'
      ? 'https://npck.kz/kk/klient-bolu-t-rtibi/'
      : lang === 'en'
        ? 'https://npck.kz/en/how-to-become-a-client-2/'
        : 'https://npck.kz/kak-stat-klientom-2/'

  return (
    <div className="appeal-page">
      {/* Шаг 1: Стать клиентом */}
      <div className="appeal-step">
        <div className="appeal-step-num">1</div>
        <div className="appeal-step-body">
          <div className="appeal-step-title">{t('appeal.step1')}</div>

          <div className="appeal-option-card">
            <div className="appeal-option-header">
              <div className="appeal-option-icon new">
                <UserPlus size={18} />
              </div>
              <div className="appeal-option-label">{t('appeal.newClientLabel')}</div>
            </div>
            <p className="appeal-option-desc">
              {t('appeal.newClientDesc')}
            </p>
            <div className="appeal-option-meta">
              <span>{t('appeal.newClientMeta')}</span>
            </div>
            <div className="appeal-option-actions">
              <a
                href={instructionUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="appeal-option-btn btn-green"
              >
                <ExternalLink size={14} />
                {t('appeal.instruction')}
              </a>
              <a
                href="/Шаблон.docx?v=2"
                download="Шаблон_заявления_НПК.docx"
                className="appeal-option-btn btn-green-outline"
              >
                <Download size={14} />
                {t('appeal.template')}
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Шаг 2: Подать обращение */}
      <div className="appeal-step">
        <div className="appeal-step-num">2</div>
        <div className="appeal-step-body">
          <div className="appeal-step-title">{t('appeal.step2')}</div>

          <div className="appeal-option-card">
            <div className="appeal-option-header">
              <div className="appeal-option-icon existing">
                <img src="/icons8-client-64.png" alt="Клиент" className="appeal-option-img" />
              </div>
              <div className="appeal-option-label">{t('appeal.existingClientLabel')}</div>
            </div>
            <p className="appeal-option-desc">
              {t('appeal.existingClientDesc')}
            </p>
            <div className="appeal-option-meta">
              <span>{t('appeal.existingClientMeta1')}</span>
              <span className="dot" />
              <span>{t('appeal.existingClientMeta2')}</span>
            </div>
            <a
              href="http://app.help-desk.kisc.kz/otrs/customer.pl?M=10&Actions=ServiceCatalogue&Param=%7B%22SearchString%22%3A%22%22%2C%22ServiceID%22%3A%22%22%2C%22TopService%22%3A%5B%222%22%2C%223%22%2C%224%22%2C%225%22%5D%2C%22ServiceIDTT%22%3A%22%22%7D"
              target="_blank"
              rel="noopener noreferrer"
              className="appeal-option-btn btn-gold"
            >
              <Globe size={14} />
              {t('appeal.personalCabinet')}
            </a>
          </div>
        </div>
      </div>

      {/* Подсказка */}
      <div className="appeal-bottom-hint">
        <Phone size={12} />
        <span>
          {t('appeal.hint')} <strong>+7 727 297 91 00</strong>
        </span>
      </div>
    </div>
  )
}
