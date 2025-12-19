"use client";

import { useTranslation } from "@/i18n/useTranslation";
import { Locale } from "@/i18n/I18nProvider";

const buttonStyle: React.CSSProperties = {
  padding: "6px 12px",
  borderRadius: 6,
  border: "1px solid #ccc",
  background: "white",
  cursor: "pointer",
};

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useTranslation();

  const changeLocale = (nextLocale: Locale) => {
    setLocale(nextLocale);
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span style={{ fontWeight: 600 }}>{t("layout.language")}</span>
      <button
        style={{
          ...buttonStyle,
          fontWeight: locale === "en" ? 700 : 400,
          opacity: locale === "en" ? 1 : 0.8,
        }}
        onClick={() => changeLocale("en")}
      >
        {t("layout.english")}
      </button>
      <button
        style={{
          ...buttonStyle,
          fontWeight: locale === "fa" ? 700 : 400,
          opacity: locale === "fa" ? 1 : 0.8,
        }}
        onClick={() => changeLocale("fa")}
      >
        {t("layout.farsi")}
      </button>
    </div>
  );
}
