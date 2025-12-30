"use client";

import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "@/i18n/useTranslation";
import { useLivestock } from "@/ui/hooks/useLivestock";
import { useIncidents } from "@/ui/hooks/useIncidents";
import { useFarms } from "@/ui/hooks/useFarms";
import { useTelemetrySeries } from "@/ui/hooks/useTelemetrySeries";
import { useCommands } from "@/ui/hooks/useCommands";
import { useHealthRisks } from "@/ui/hooks/useHealthRisks";
import { useDashboardKpis } from "@/ui/hooks/useDashboardKpis";
import { useSeedPreference } from "@/ui/hooks/useSeedPreference";
import { KpiCard } from "@/ui/components/KpiCard";
import { LiveStatusPanel } from "@/ui/components/LiveStatusPanel";
import { TelemetryChart } from "@/ui/components/TelemetryChart";
import { HealthRiskOverview } from "@/ui/components/HealthRiskOverview";
import { CommandPanel } from "@/ui/components/CommandPanel";
import { IncidentsTimeline } from "@/ui/components/IncidentsTimeline";
import { SectionCard } from "@/ui/components/SectionCard";
import { SeedDataToggle } from "@/ui/components/SeedDataToggle";
import styles from "@/ui/styles/dashboard.module.css";

export default function DashboardPage() {
  const { t } = useTranslation();
  const { useSeed, setUseSeed, hydrated } = useSeedPreference();
  const { data: farms, source: farmsSource } = useFarms({ useSeed });
  const {
    data: livestock,
    loading: livestockLoading,
    source: livestockSource,
  } = useLivestock({ useSeed });
  const {
    data: incidents,
    loading: incidentsLoading,
    source: incidentsSource,
  } = useIncidents({ useSeed });
  const {
    data: telemetrySeries,
    loading: telemetryLoading,
    source: telemetrySource,
  } = useTelemetrySeries({ useSeed });
  const {
    data: commands,
    loading: commandsLoading,
    source: commandsSource,
  } = useCommands({ useSeed });
  const {
    data: healthRisks,
    loading: healthLoading,
    source: healthSource,
  } = useHealthRisks({ useSeed });

  const [selectedLivestockId, setSelectedLivestockId] = useState<string | null>(
    null
  );

  useEffect(() => {
    if (!selectedLivestockId && livestock.length > 0) {
      setSelectedLivestockId(livestock[0].id);
    }
  }, [livestock, selectedLivestockId]);

  const dataSource = useMemo(() => {
    if (useSeed) return "seed";
    const sources = [
      farmsSource,
      livestockSource,
      incidentsSource,
      telemetrySource,
      commandsSource,
      healthSource,
    ];
    return sources.includes("seed") ? "seed" : "live";
  }, [
    useSeed,
    farmsSource,
    livestockSource,
    incidentsSource,
    telemetrySource,
    commandsSource,
    healthSource,
  ]);

  const kpis = useDashboardKpis({ farms, livestock, incidents });

  return (
    <div className={styles.dashboardPage}>
      <div className={styles.pageHeader}>
        <div>
          <p className={styles.pageEyebrow}>{t("dashboard.subtitle")}</p>
          <h1 className={styles.pageTitle}>{t("dashboard.title")}</h1>
          <p className={styles.pageDescription}>{t("dashboard.description")}</p>
        </div>
        <div className={styles.pageActions}>
          <SeedDataToggle
            checked={useSeed}
            onChange={setUseSeed}
            disabled={!hydrated}
            dataSource={dataSource}
          />
        </div>
      </div>

      <section className={styles.kpiGrid}>
        <KpiCard
          label={t("kpi.activeFarms")}
          value={kpis.activeFarms}
          delta={t("kpi.activeFarms.delta")}
          tone="primary"
        />
        <KpiCard
          label={t("kpi.onlineLivestock")}
          value={kpis.onlineLivestock}
          delta={t("kpi.onlineLivestock.delta")}
          tone="success"
        />
        <KpiCard
          label={t("kpi.activeAlerts")}
          value={kpis.activeAlerts}
          delta={t("kpi.activeAlerts.delta")}
          tone="danger"
        />
        <KpiCard
          label={t("kpi.systemHealth")}
          value={`${kpis.systemHealth}%`}
          delta={t("kpi.systemHealth.delta")}
          tone="warning"
        />
      </section>

      <div className={styles.primaryGrid}>
        <SectionCard
          id="livestatus"
          title={t("livestatus.title")}
          subtitle={t("livestatus.subtitle")}
        >
          <LiveStatusPanel
            livestock={livestock}
            selectedLivestockId={selectedLivestockId}
            onSelectLivestock={setSelectedLivestockId}
            useSeed={useSeed}
            loading={livestockLoading}
          />
        </SectionCard>

        <SectionCard
          id="telemetry"
          title={t("telemetry.title")}
          subtitle={t("telemetry.subtitle")}
        >
          <TelemetryChart
            loading={telemetryLoading}
            series={telemetrySeries}
          />
        </SectionCard>
      </div>

      <div className={styles.secondaryGrid}>
        <SectionCard
          id="health"
          title={t("health.title")}
          subtitle={t("health.subtitle")}
        >
          <HealthRiskOverview loading={healthLoading} risks={healthRisks} />
        </SectionCard>
        <SectionCard
          id="commands"
          title={t("commands.title")}
          subtitle={t("commands.subtitle")}
        >
          <CommandPanel loading={commandsLoading} commands={commands} />
        </SectionCard>
      </div>

      <SectionCard
        id="incidents"
        title={t("incidents.title")}
        subtitle={t("incidents.subtitle")}
      >
        <IncidentsTimeline
          loading={incidentsLoading}
          incidents={incidents}
        />
      </SectionCard>
    </div>
  );
}
