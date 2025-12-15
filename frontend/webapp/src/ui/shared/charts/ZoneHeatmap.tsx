'use client'

export function ZoneHeatmap({
  values,
  title,
}: {
  title: string
  values: Record<string, number | null>
}) {
  const entries = Object.entries(values)

  return (
    <div className="space-y-3">
      <h3 className="font-semibold">{title}</h3>

      <div className="grid grid-cols-3 gap-3">
        {entries.map(([zoneId, v]) => (
          <div key={zoneId} className="rounded-xl border p-3">
            <div className="text-xs text-gray-500">{zoneId}</div>
            <div className="text-xl font-semibold">
              {v === null ? '—' : v.toFixed(1)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
