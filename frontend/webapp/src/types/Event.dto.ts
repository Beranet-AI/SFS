import { UUID, ISODateString } from './Core.types'
import { SensorMetric } from './Device.dto'

export type EventSeverity = 'info' | 'warning' | 'critical'
export type EventStatus = 'raised' | 'ack' | 'resolved'

export interface Event {
  id: UUID

  severity: EventSeverity
  status: EventStatus

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
