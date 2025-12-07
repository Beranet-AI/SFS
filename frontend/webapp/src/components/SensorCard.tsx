
///frontend/webapp/src/components/SensorCard.tsx


import React from "react";
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

export default function SensorCard({
  name,
  faLabel,
  unit,
  icon,
  color = '#facc15',
  reading,
  alert,
}: SensorCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900/60 p-4 shadow hover:shadow-lg hover:border-slate-500 transition">
      <h2 className="text-lg font-medium mb-1 flex items-center gap-2">
        {icon && <span className="text-xl">{icon}</span>}
        {name} {faLabel && `(${faLabel})`}
      </h2>
      {alert && (
        <div className="mb-2 rounded-lg border border-red-500/60 bg-red-900/30 px-3 py-2 text-sm text-red-100">
          <p className="font-semibold">هشدار فعال</p>
          <p className="text-xs leading-relaxed">{alert.message}</p>
          <p className="text-[11px] text-red-200/80 mt-1">زمان: {new Date(alert.raised_at).toLocaleString()}</p>
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