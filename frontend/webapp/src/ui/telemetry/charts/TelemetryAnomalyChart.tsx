'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Scatter,
} from 'recharts'
import type { TelemetryReading } from '@/types/Telemetry.dto'

interface Props {
  readings: TelemetryReading[]
  anomalies?: string[] // list of telemetry IDs
}

export function TelemetryAnomalyChart({ readings, anomalies = [] }: Props) {
  const data = readings.map((r) => ({
    id: r.id,
    time: new Date(r.timestamp).toLocaleTimeString(),
    value: r.value,
    anomaly: anomalies.includes(r.id) ? r.value : null,
  }))

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" dot={false} />
          <Scatter dataKey="anomaly" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
