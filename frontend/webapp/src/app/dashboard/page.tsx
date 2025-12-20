"use client";

import '../globals.css'; 

import { LiveStatusPanel } from "@/ui/components/LiveStatusPanel";
import { IncidentsTable } from "@/ui/components/IncidentsTable";
import { LivestockTable } from "@/ui/components/LivestockTable";
import { useTranslation } from "@/i18n/useTranslation";

export default function DashboardPage() {
  const { t } = useTranslation();

  return (
    <main style={{ display: "grid", gap: 16 }}>
      <h1>{t("dashboard.title")}</h1>
      <LiveStatusPanel />
      <IncidentsTable />
      <LivestockTable />
    </main>
  );
}
