"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import en from "@/i18n/locales/en/common.json";
import fa from "@/i18n/locales/fa/common.json";

export type Locale = "en" | "fa";
export type Messages = Record<string, string>;

const STORAGE_KEY = "sfs.locale";

const dictionaries: Record<Locale, Messages> = {
  en,
  fa,
};

type I18nContextValue = {
  locale: Locale;
  direction: "ltr" | "rtl";
  t: (key: string) => string;
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

  const messages = useMemo(() => dictionaries[locale] ?? en, [locale]);
  const translate = (key: string) => messages[key] ?? en[key] ?? key;
  const direction = locale === "fa" ? "rtl" : "ltr";

  return (
    <I18nContext.Provider value={{ locale, direction, t: translate, setLocale }}>
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
