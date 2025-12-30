"use client";

import type { Incident } from "@/domain/models/Incident";
import { useTranslation } from "@/i18n/useTranslation";
import { formatDateTime } from "@/ui/utils/formatters";
import { EmptyState } from "@/ui/components/EmptyState";
import { Skeleton } from "@/ui/components/Skeleton";
import { StatusBadge } from "@/ui/components/StatusBadge";
import styles from "@/ui/styles/dashboard.module.css";

type IncidentsTimelineProps = {
  incidents: Incident[];
  loading?: boolean;
};

export function IncidentsTimeline({ incidents, loading }: IncidentsTimelineProps) {
  const { t, locale } = useTranslation();

  if (loading) {
    return (
      <div className={styles.timeline}>
        <Skeleton />
        <Skeleton width="80%" />
        <Skeleton width="70%" />
      </div>
    );
  }

  if (incidents.length === 0) {
    return <EmptyState message={t("incidents.empty")} />;
  }

  return (
    <div className={styles.timeline}>
      {incidents.map((incident) => (
        <div key={incident.id} className={styles.timelineItem}>
          <span
            className={styles.timelineDot}
            style={{
              background:
                incident.severity === "critical"
                  ? "var(--danger)"
                  : incident.severity === "high"
                  ? "var(--warning)"
                  : "var(--primary)",
            }}
          />
          <div className={styles.timelineContent}>
            <div className={styles.timelineTitle}>
              {incident.description}
            </div>
            <div className={styles.timelineMeta}>
              {t("incidents.timelineLabel")} {incident.livestockId} ·{" "}
              {formatDateTime(incident.createdAt, locale)}
            </div>
            <div className={styles.statusHeader}>
              <StatusBadge
                tone={incident.severity}
                label={t(`incidents.severity.${incident.severity}` as never)}
              />
              <StatusBadge
                tone={incident.status === "resolved" ? "success" : "warning"}
                label={t(`incidents.status.${incident.status}` as never)}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
