"use client";

import type { HealthRisk } from "@/domain/models/HealthRisk";
import { useTranslation } from "@/i18n/useTranslation";
import { formatDateTime } from "@/ui/utils/formatters";
import { EmptyState } from "@/ui/components/EmptyState";
import { Skeleton } from "@/ui/components/Skeleton";
import { StatusBadge } from "@/ui/components/StatusBadge";
import styles from "@/ui/styles/dashboard.module.css";

type HealthRiskOverviewProps = {
  risks: HealthRisk[];
  loading?: boolean;
};

export function HealthRiskOverview({ risks, loading }: HealthRiskOverviewProps) {
  const { t, locale } = useTranslation();

  if (loading) {
    return (
      <div className={styles.liveStatusList}>
        <Skeleton />
        <Skeleton width="70%" />
        <Skeleton width="85%" />
      </div>
    );
  }

  if (risks.length === 0) {
    return <EmptyState message={t("health.empty")} />;
  }

  return (
    <table className={styles.table}>
      <thead>
        <tr>
          <th>{t("health.table.livestock")}</th>
          <th>{t("health.table.risk")}</th>
          <th>{t("health.table.score")}</th>
          <th>{t("health.table.updated")}</th>
        </tr>
      </thead>
      <tbody>
        {risks.map((risk) => (
          <tr key={risk.id}>
            <td>{risk.livestockTag}</td>
            <td>
              <StatusBadge tone={risk.riskLevel} label={t(`risk.${risk.riskLevel}` as never)} />
            </td>
            <td>{risk.score}</td>
            <td>{formatDateTime(risk.lastEvaluatedAt, locale)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
