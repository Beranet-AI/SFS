'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ReferenceLine,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import type { TelemetryReading } from '@/types/Telemetry.dto'

interface Props {
  readings: TelemetryReading[]
  minSafe?: number
  maxSafe?: number
}

export function TelemetryThresholdChart({ readings, minSafe, maxSafe }: Props) {
  const data = readings.map((r) => ({
    time: new Date(r.timestamp).toLocaleTimeString(),
    value: r.value,
  }))

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          {minSafe !== undefined && (
            <ReferenceLine y={minSafe} strokeDasharray="4 4" label="Min Safe" />
          )}
          {maxSafe !== undefined && (
            <ReferenceLine y={maxSafe} strokeDasharray="4 4" label="Max Safe" />
          )}
          <Line type="monotone" dataKey="value" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
