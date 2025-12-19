"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import en from "@/i18n/locales/en/common.json";
import fa from "@/i18n/locales/fa/common.json";

/**
 * Translation keys are derived from the EN dictionary (source of truth)
 */
export type TranslationKey = keyof typeof en;

export type Locale = "en" | "fa";

/**
 * Messages must strictly follow TranslationKey
 */
export type Messages = Record<TranslationKey, string>;

const STORAGE_KEY = "sfs.locale";

/**
 * Dictionaries must conform to Messages
 */
const dictionaries: Record<Locale, Messages> = {
  en: en as Messages,
  fa: fa as Messages,
};

type I18nContextValue = {
  locale: Locale;
  direction: "ltr" | "rtl";
  t: (key: TranslationKey) => string;
  setLocale: (locale: Locale) => void;
};

const I18nContext = createContext<I18nContextValue | undefined>(undefined);

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>(() => {
    if (typeof window === "undefined") return "en";
    const stored = window.localStorage.getItem(STORAGE_KEY) as Locale | null;
    return stored === "fa" || stored === "en" ? stored : "en";
  });

  useEffect(() => {
    const dir = locale === "fa" ? "rtl" : "ltr";
    document.documentElement.lang = locale;
    document.documentElement.dir = dir;
    window.localStorage.setItem(STORAGE_KEY, locale);
  }, [locale]);

  const messages = useMemo<Messages>(
    () => dictionaries[locale] ?? dictionaries.en,
    [locale]
  );

  const translate = (key: TranslationKey): string => {
    return messages[key] ?? dictionaries.en[key];
  };

  const direction = locale === "fa" ? "rtl" : "ltr";

  return (
    <I18nContext.Provider
      value={{
        locale,
        direction,
        t: translate,
        setLocale,
      }}
    >
      <div dir={direction}>{children}</div>
    </I18nContext.Provider>
  );
}

export function useI18nContext() {
  const ctx = useContext(I18nContext);
  if (!ctx) {
    throw new Error("useI18nContext must be used within I18nProvider");
  }
  return ctx;
}
