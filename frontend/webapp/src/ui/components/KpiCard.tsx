"use client";

import styles from "@/ui/styles/dashboard.module.css";

type KpiCardProps = {
  label: string;
  value: string | number;
  delta?: string;
  tone?: "primary" | "success" | "danger" | "warning";
};

export function KpiCard({ label, value, delta, tone }: KpiCardProps) {
  const toneClass =
    tone === "success"
      ? styles.kpiToneSuccess
      : tone === "danger"
      ? styles.kpiToneDanger
      : tone === "warning"
      ? styles.kpiToneWarning
      : styles.kpiTonePrimary;

  return (
    <div className={styles.kpiCard}>
      <span className={styles.kpiLabel}>{label}</span>
      <span className={`${styles.kpiValue} ${toneClass}`}>{value}</span>
      {delta ? <span className={styles.kpiDelta}>{delta}</span> : null}
    </div>
  );
}
