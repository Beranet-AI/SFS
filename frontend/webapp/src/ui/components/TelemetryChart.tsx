"use client";

import type { TelemetrySeries } from "@/domain/models/Telemetry";
import { useTranslation } from "@/i18n/useTranslation";
import { formatDateTime } from "@/ui/utils/formatters";
import { EmptyState } from "@/ui/components/EmptyState";
import { Skeleton } from "@/ui/components/Skeleton";
import styles from "@/ui/styles/dashboard.module.css";

type TelemetryChartProps = {
  series: TelemetrySeries[];
  loading?: boolean;
};

const palette = ["#1b66f6", "#21b07d", "#e68619", "#d64545"];

function buildPolyline(points: { x: number; y: number }[]) {
  return points.map((point) => `${point.x},${point.y}`).join(" ");
}

export function TelemetryChart({ series, loading }: TelemetryChartProps) {
  const { t, locale } = useTranslation();

  if (loading) {
    return (
      <div className={styles.chartWrapper}>
        <Skeleton />
        <Skeleton width="70%" />
        <Skeleton width="90%" />
      </div>
    );
  }

  if (series.length === 0) {
    return <EmptyState message={t("telemetry.empty")} />;
  }

  const flattened = series.flatMap((metric) => metric.points);
  const timestamps = flattened.map((point) => new Date(point.timestamp).getTime());
  const minX = Math.min(...timestamps);
  const maxX = Math.max(...timestamps);
  const values = flattened.map((point) => point.value);
  const minY = Math.min(...values);
  const maxY = Math.max(...values);

  const height = 180;
  const width = 560;

  return (
    <div className={styles.chartWrapper}>
      <svg viewBox={`0 0 ${width} ${height}`} className={styles.chartSvg}>
        {series.map((metric, index) => {
          const points = metric.points.map((point) => {
            const x =
              ((new Date(point.timestamp).getTime() - minX) / (maxX - minX || 1)) *
              (width - 40) +
              20;
            const y =
              height -
              (((point.value - minY) / (maxY - minY || 1)) * (height - 30) + 15);
            return { x, y };
          });
          return (
            <polyline
              key={metric.metric}
              fill="none"
              stroke={palette[index % palette.length]}
              strokeWidth="2"
              points={buildPolyline(points)}
            />
          );
        })}
      </svg>
      <div className={styles.chartLegend}>
        {series.map((metric, index) => (
          <div key={metric.metric} className={styles.legendItem}>
            <span
              className={styles.legendDot}
              style={{ background: palette[index % palette.length] }}
            />
            <span>
              {metric.metric} · {metric.unit}
            </span>
          </div>
        ))}
        {series[0]?.points?.length ? (
          <span className={styles.seedHint}>
            {t("telemetry.rangeLabel")}{" "}
            {formatDateTime(series[0].points[0].timestamp, locale)} —{" "}
            {formatDateTime(
              series[0].points[series[0].points.length - 1].timestamp,
              locale
            )}
          </span>
        ) : null}
      </div>
    </div>
  );
}
