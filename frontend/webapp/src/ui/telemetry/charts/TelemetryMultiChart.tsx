'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import type { TelemetryReading } from '@/types/Telemetry.dto'

interface Props {
  readings: TelemetryReading[]
  metrics: string[]
}

export function TelemetryMultiChart({ readings, metrics }: Props) {
  const data = readings.reduce<Record<string, number | string>[]>((acc, r) => {
    const last = acc[acc.length - 1]
    const time = new Date(r.timestamp).toLocaleTimeString()

    if (!last || last.time !== time) {
      acc.push({ time, [r.metric]: r.value })
    } else {
      last[r.metric] = r.value
    }

    return acc
  }, [])

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          {metrics.map((m) => (
            <Line
              key={m}
              type="monotone"
              dataKey={m}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
