import { UUID, ISODateString } from './Core.types'
import { SensorMetric } from './Device.dto'

export type IncidentSeverity = 'info' | 'warning' | 'critical'
export type IncidentStatus = 'raised' | 'ack' | 'resolved'

export interface Incident {
  id: UUID

  severity: IncidentSeverity
  status: IncidentStatus

  metric?: SensorMetric
  value?: number

  title: string
  message: string

  farmId: UUID
  barnId?: UUID
  zoneId?: UUID
  deviceId?: UUID

  createdAt: ISODateString
  updatedAt?: ISODateString
}
