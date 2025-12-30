"use client";

import { useTranslation } from "@/i18n/useTranslation";
import { LanguageSwitcher } from "@/ui/components/LanguageSwitcher";
import styles from "@/ui/styles/dashboard.module.css";

export function AppTopbar() {
  const { t } = useTranslation();

  return (
    <header className={styles.topbar}>
      <div className={styles.topbarGroup}>
        <span className={`${styles.badge} ${styles.badgePrimary}`}>
          {t("layout.envProduction")}
        </span>
        <span className={styles.badge}>{t("layout.systemStatus")}</span>
      </div>
      <div className={styles.topbarGroup}>
        <LanguageSwitcher />
      </div>
    </header>
  );
}
