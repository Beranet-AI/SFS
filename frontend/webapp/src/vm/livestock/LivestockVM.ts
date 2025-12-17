export interface LivestockVM {
  id: string

  /** Identity */
  displayName: string

  /** Health summary */
  healthStatus: 'healthy' | 'warning' | 'critical'
  healthLabel: string

  /** Telemetry highlight */
  primaryMetricLabel?: string
  primaryMetricValue?: string

  /** Live Status */
  hasActiveLiveStatus: boolean
  highestLiveStatusSeverity?: 'warning' | 'critical'

  /** Activity */
  lastSeenLabel: string
}
