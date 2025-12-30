"use client";

import { useTranslation } from "@/i18n/useTranslation";
import { Locale } from "@/i18n/I18nProvider";
import styles from "@/ui/styles/dashboard.module.css";

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useTranslation();

  const changeLocale = (nextLocale: Locale) => {
    setLocale(nextLocale);
  };

  return (
    <div className={styles.topbarGroup}>
      <span className={styles.seedHint}>{t("layout.language")}</span>
      <button
        className={`${styles.button} ${
          locale === "en" ? styles.buttonActive : ""
        }`}
        onClick={() => changeLocale("en")}
      >
        {t("layout.english")}
      </button>
      <button
        className={`${styles.button} ${
          locale === "fa" ? styles.buttonActive : ""
        }`}
        onClick={() => changeLocale("fa")}
      >
        {t("layout.farsi")}
      </button>
    </div>
  );
}
