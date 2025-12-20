"use client";

import './globals.css'; 
import { useTranslation } from "@/i18n/useTranslation";

export default function HomePage() {
  const { t } = useTranslation();

  return (
    <main style={{ padding: 16 }}>
      <h1>{t("app.title")}</h1>
      <p>{t("app.cta")}</p>
    </main>
  );
}
