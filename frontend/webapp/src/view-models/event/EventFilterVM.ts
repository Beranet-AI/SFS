export interface EventFilterVM {
  severities: Array<'info' | 'warning' | 'critical'>
  statuses: Array<'raised' | 'ack' | 'resolved'>

  fromDate?: string
  toDate?: string

  deviceId?: string
  zoneId?: string
}
