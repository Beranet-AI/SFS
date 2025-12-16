import { IncidentSeverity } from '@/types/Incident.dto'

export function LiveStatusBadge({ severity }: { severity: IncidentSeverity }) {
  const color =
    severity === 'critical'
      ? 'bg-red-600'
      : severity === 'warning'
        ? 'bg-yellow-500'
        : 'bg-blue-500'

  return (
    <span className={`rounded px-2 py-0.5 text-xs text-white ${color}`}>
      {severity.toUpperCase()}
    </span>
  )
}
