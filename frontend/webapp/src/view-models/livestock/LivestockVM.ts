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

  /** Alerts */
  hasActiveAlert: boolean
  highestAlertSeverity?: 'warning' | 'critical'

  /** Activity */
  lastSeenLabel: string
}
