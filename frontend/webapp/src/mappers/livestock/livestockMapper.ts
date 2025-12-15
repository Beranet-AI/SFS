import { livestockVM } from '@/view-models/livestock/LivestockVM'
import { livestockHealthLabel } from '@/policies/livestock/livestockHealthPolicy'

interface livestockAggregateInput {
  id: string
  name: string

  healthStatus: 'healthy' | 'warning' | 'critical'

  primaryMetricLabel?: string
  primaryMetricValue?: string

  hasActiveLiveStatus: boolean
  highestLiveStatusSeverity?: 'warning' | 'critical'

  lastSeenAt?: string
}

export function mapLivestockToVM(data: livestockAggregateInput): livestockVM {
  const lastSeenLabel = data.lastSeenAt
    ? new Date(data.lastSeenAt).toLocaleString()
    : 'No recent activity'

  return {
    id: data.id,
    displayName: data.name,

    healthStatus: data.healthStatus,
    healthLabel: livestockHealthLabel(data.healthStatus),

    primaryMetricLabel: data.primaryMetricLabel,
    primaryMetricValue: data.primaryMetricValue,

    hasActiveLiveStatus: data.hasActiveAlert,
    highestLiveStatusSeverity: data.highestAlertSeverity,

    lastSeenLabel,
  }
}
