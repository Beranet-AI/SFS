"use client";

import { useMemo } from "react";
import { useTranslation } from "@/i18n/useTranslation";
import { useLiveStatus } from "@/ui/hooks/useLiveStatus";
import { useHealthDecision } from "@/ui/hooks/useHealthDecision";
import type { Livestock } from "@/domain/models/Livestock";
import { formatDateTime } from "@/ui/utils/formatters";
import { EmptyState } from "@/ui/components/EmptyState";
import { Skeleton } from "@/ui/components/Skeleton";
import styles from "@/ui/styles/dashboard.module.css";

type LiveStatusPanelProps = {
  livestock: Livestock[];
  selectedLivestockId: string | null;
  onSelectLivestock: (id: string) => void;
  useSeed: boolean;
  loading: boolean;
};

export function LiveStatusPanel({
  livestock,
  selectedLivestockId,
  onSelectLivestock,
  useSeed,
  loading,
}: LiveStatusPanelProps) {
  const { t, locale } = useTranslation();
  const { data, loading: liveLoading } = useLiveStatus(
    selectedLivestockId ?? undefined,
    { useSeed }
  );
  const { run, loading: decisionLoading } = useHealthDecision();

  const livestockOptions = useMemo(
    () =>
      livestock.map((item) => ({
        id: item.id,
        label: `${item.tag} · ${item.barn} / ${item.zone}`,
      })),
    [livestock]
  );

  if (!loading && livestockOptions.length === 0) {
    return <EmptyState message={t("livestatus.empty")} />;
  }

  return (
    <div>
      <div className={styles.statusHeader}>
        <select
          className={styles.select}
          value={selectedLivestockId ?? ""}
          onChange={(event) => onSelectLivestock(event.target.value)}
        >
          {livestockOptions.map((item) => (
            <option key={item.id} value={item.id}>
              {item.label}
            </option>
          ))}
        </select>
        <button
          className={styles.button}
          onClick={() => selectedLivestockId && run(selectedLivestockId)}
          disabled={decisionLoading || !selectedLivestockId}
        >
          {t("livestatus.runDecision")}
        </button>
      </div>

      {loading || liveLoading ? (
        <div className={styles.liveStatusList}>
          <Skeleton />
          <Skeleton width="80%" />
          <Skeleton width="60%" />
        </div>
      ) : data.length === 0 ? (
        <EmptyState message={t("livestatus.empty")} />
      ) : (
        <div className={styles.liveStatusList}>
          {data.slice(-5).map((item, index) => (
            <div key={`${item.metric}-${index}`} className={styles.liveStatusItem}>
              <div>
                <div className={styles.metricLabel}>{item.metric}</div>
                <div className={styles.metricMeta}>
                  {formatDateTime(item.recordedAt, locale)}
                </div>
              </div>
              <div className={styles.metricLabel}>{item.value}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
