import { EventSeverity } from '@/types/Event.dto'

export function AlertBadge({ severity }: { severity: EventSeverity }) {
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
