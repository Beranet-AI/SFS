export interface EventVM {
  id: string

  /** Main display */
  title: string
  message: string

  /** Severity & status */
  severity: 'info' | 'warning' | 'critical'
  severityLabel: string
  severityColor: 'blue' | 'yellow' | 'red'

  status: 'raised' | 'ack' | 'resolved'
  statusLabel: string

  /** Source */
  sourceLabel: string

  /** Time */
  timestamp: string
}
