"use client";

import styles from "@/ui/styles/dashboard.module.css";

type SectionCardProps = {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  id?: string;
};

export function SectionCard({ title, subtitle, children, id }: SectionCardProps) {
  return (
    <section className={styles.sectionCard} id={id}>
      <header className={styles.sectionHeader}>
        <h2 className={styles.sectionTitle}>{title}</h2>
        {subtitle ? <p className={styles.sectionSubtitle}>{subtitle}</p> : null}
      </header>
      {children}
    </section>
  );
}
