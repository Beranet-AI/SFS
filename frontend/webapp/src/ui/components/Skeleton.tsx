"use client";

import styles from "@/ui/styles/dashboard.module.css";

export function Skeleton({ width }: { width?: string }) {
  return <div className={styles.skeleton} style={{ width: width ?? "100%" }} />;
}
