import { createContext, useContext, useState, useCallback, ReactNode } from 'react'
import type { Lang } from './translations'

const STORAGE_KEY = 'npck_lang'

interface I18nCtx {
  lang: Lang
  setLang: (l: Lang) => void
}

const I18nContext = createContext<I18nCtx | null>(null)

function getInitialLang(): Lang {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw === 'ru' || raw === 'kz' || raw === 'en') return raw
  } catch {}
  return 'ru'
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(getInitialLang)

  const setLang = useCallback((l: Lang) => {
    setLangState(l)
    try {
      localStorage.setItem(STORAGE_KEY, l)
    } catch {}
  }, [])

  return (
    <I18nContext.Provider value={{ lang, setLang }}>
      {children}
    </I18nContext.Provider>
  )
}

export function useI18n() {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error('useI18n must be used within I18nProvider')
  return ctx
}
