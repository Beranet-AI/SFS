'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import type { TelemetryReading } from '@/types/Telemetry.dto'

interface Props {
  data?: TelemetryReading[]
}

export function TelemetryChart({ data = [] }: Props) {
  const chartData = data.map((r) => ({
    time: new Date(r.timestamp).toLocaleTimeString(),
    value: r.value,
  }))

  if (chartData.length === 0) {
    return (
      <div className="h-64 w-full flex items-center justify-center text-sm text-muted-foreground">
        No telemetry data
      </div>
    )
  }

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
