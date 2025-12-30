"use client";

import styles from "@/ui/styles/dashboard.module.css";

type StatusBadgeProps = {
  label: string;
  tone?: "low" | "medium" | "high" | "critical" | "success" | "warning" | "danger";
};

export function StatusBadge({ label, tone }: StatusBadgeProps) {
  const toneClass =
    tone === "critical" || tone === "danger"
      ? styles.badgeDanger
      : tone === "high" || tone === "warning"
      ? styles.badgeWarning
      : styles.badgePrimary;

  return <span className={`${styles.badge} ${toneClass}`}>{label}</span>;
}
