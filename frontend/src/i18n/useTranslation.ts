import { useCallback } from 'react'
import { useI18n } from './I18nContext'
import { translations } from './translations'

export function useTranslation() {
  const { lang } = useI18n()

  const t = useCallback(
    (key: string) => {
      const dict = translations[lang]
      return dict[key] ?? translations.ru[key] ?? key
    },
    [lang]
  )

  return { t, lang }
}
