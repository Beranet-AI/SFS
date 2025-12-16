import { UUID, ISODateString } from './Core.types'

export type DeviceKind =
  | 'sensor'
  | 'camera'
  | 'rfid'
  | 'motion_sensor'
  | 'gateway'
  | 'other'

export type SensorMetric =
  | 'temperature'
  | 'humidity'
  | 'ammonia'
  | 'heart_rate'
  | 'movement_score'
  | 'weight'
  | 'milk_yield'

export interface Device {
  id: UUID

  farmId: UUID
  barnId: UUID | null
  zoneId: UUID | null

  name: string
  kind: DeviceKind

  ipAddress: string | null

  metrics?: SensorMetric[]

  isActive: boolean
  createdAt: ISODateString
}
