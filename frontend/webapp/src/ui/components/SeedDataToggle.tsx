"use client";

import { useTranslation } from "@/i18n/useTranslation";
import styles from "@/ui/styles/dashboard.module.css";

type SeedDataToggleProps = {
  checked: boolean;
  onChange: (next: boolean) => void;
  disabled?: boolean;
  dataSource: "live" | "seed";
};

export function SeedDataToggle({
  checked,
  onChange,
  disabled,
  dataSource,
}: SeedDataToggleProps) {
  const { t } = useTranslation();

  return (
    <div className={styles.toggle}>
      <label className={styles.seedHint}>{t("seed.toggleLabel")}</label>
      <input
        className={styles.toggleInput}
        type="checkbox"
        checked={checked}
        disabled={disabled}
        onChange={(event) => onChange(event.target.checked)}
        aria-label={t("seed.toggleAriaLabel")}
      />
      <span
        className={`${styles.badge} ${
          dataSource === "seed" ? styles.badgeWarning : styles.badgePrimary
        }`}
      >
        {dataSource === "seed" ? t("seed.demo") : t("seed.live")}
      </span>
    </div>
  );
}
