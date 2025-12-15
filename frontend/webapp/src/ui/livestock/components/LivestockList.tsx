import type { LivestockVM } from '@/view-models/livestock/LivestockVM'

interface Props {
  livestock: LivestockVM[]
}

export function LivestockList({ livestock }: Props) {
  if (!livestock.length) {
    return <div className="text-sm text-gray-500">No livestock</div>
  }

  return (
    <div className="grid grid-cols-1 gap-3">
      {livestock.map((animal) => (
        <div
          key={animal.id}
          className="rounded border p-3 flex justify-between"
        >
          <div>
            <div className="font-medium">{animal.displayName}</div>
            <div className="text-xs text-gray-500">
              Last seen: {animal.lastSeenLabel}
            </div>
          </div>

          <div className="text-right">
            <div
              className={`text-sm font-semibold ${
                animal.healthStatus === 'critical'
                  ? 'text-red-600'
                  : animal.healthStatus === 'warning'
                    ? 'text-yellow-600'
                    : 'text-green-600'
              }`}
            >
              {animal.healthLabel}
            </div>

            {animal.primaryMetricValue && (
              <div className="text-xs text-gray-500">
                {animal.primaryMetricLabel}: {animal.primaryMetricValue}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
