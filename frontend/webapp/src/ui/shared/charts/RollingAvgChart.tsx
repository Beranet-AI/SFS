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

export function RollingAvgChart({
  series,
}: {
  series: Array<{ time: string; raw: number; avg: number | null }>
}) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={series}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="raw" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="avg" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
