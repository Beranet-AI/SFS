
///frontend/webapp/src/components/SensorCard.tsx


import React, { useMemo } from "react";
import useSWR from "swr";
import SensorChart from "./SensorChart";

type AlertInfo = {
  severity: "info" | "warn" | "critical";
  message: string;
  raised_at: string;
};

export type SensorCardProps = {
  name: string;
  faLabel?: string;
  unit?: string;
  icon?: string;
  color?: string;
  reading: {
    sensor: number;
    ts: string;
    value: number;
    quality: string;
  } | null;
  alert?: AlertInfo | null;
};

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function SensorCard({
  name,
  faLabel,
  unit,
  icon,
  color = "#facc15",
  reading,
  alert,
}: SensorCardProps) {
  const sensorId = reading?.sensor;
  const { data: alertsData } = useSWR(
    sensorId ? `/api/alerts/active?sensor_id=${sensorId}` : null,
    fetcher,
    { refreshInterval: 5000 }
  );

  const activeAlert: AlertInfo | null = useMemo(() => {
    if (alert) return alert;
    const latest = alertsData?.alerts?.[0];
    if (!latest) return null;
    return {
      severity: "warn",
      message: `مقدار سنسور از حد مجاز عبور کرده است (${latest.value})`,
      raised_at: latest.triggered_at,
    };
  }, [alert, alertsData]);

  const containerClasses = [
    "rounded-xl border bg-slate-900/60 p-4 shadow hover:shadow-lg transition",
    activeAlert ? "border-red-500/70 shadow-red-500/40" : "border-slate-700 hover:border-slate-500",
  ].join(" ");

  return (
    <div className={containerClasses}>
      <h2 className="text-lg font-medium mb-1 flex items-center gap-2">
        {icon && <span className="text-xl">{icon}</span>}
        {name} {faLabel && `(${faLabel})`}
      </h2>
      {activeAlert && (
        <div className="mb-2 rounded-lg border border-red-500/60 bg-red-900/30 px-3 py-2 text-sm text-red-100">
          <p className="font-semibold">هشدار فعال</p>
          <p className="text-xs leading-relaxed">{activeAlert.message}</p>
          <p className="text-[11px] text-red-200/80 mt-1">زمان: {new Date(activeAlert.raised_at).toLocaleString()}</p>
        </div>
      )}
      {reading ? (
        <>
          <p className="text-3xl font-semibold">
            {reading.value.toFixed(2)} <span className="text-base text-slate-400">{unit}</span>
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Sensor ID: {reading.sensor} | کیفیت: {reading.quality}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Last update: {new Date(reading.ts).toLocaleString()}
          </p>
          <div className="mt-2">
            <SensorChart sensorId={reading.sensor} color={color} />
          </div>
        </>
      ) : (
        <p className="text-sm text-slate-400">
          هنوز داده‌ای برای {faLabel || name} ثبت نشده است.
        </p>
      )}
    </div>
  );
}