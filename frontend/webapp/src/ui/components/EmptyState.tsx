"use client";

import styles from "@/ui/styles/dashboard.module.css";

export function EmptyState({ message }: { message: string }) {
  return <div className={styles.emptyState}>{message}</div>;
}
