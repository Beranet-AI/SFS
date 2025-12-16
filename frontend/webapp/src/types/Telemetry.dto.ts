import { UUID, ISODateString } from './Core.types'
import { SensorMetric } from './Device.dto'

export interface Telemetry {
  id: UUID

  deviceId: UUID
  metric: SensorMetric

  value: number
  unit: string

  timestamp: ISODateString
  receivedAt: ISODateString

  edgeId: UUID
}

export interface TelemetryPoint {
  timestamp: ISODateString
  value: number
}

export interface TelemetrySeries {
  metric: SensorMetric
  unit: string
  points: TelemetryPoint[]
}

/**
 * Telemetry reading DTO
 * Source of truth: Backend (FastAPI)
 */
export interface TelemetryReading {
  id: UUID

  deviceId: UUID
  metric: SensorMetric

  value: number
  unit: string

  timestamp: ISODateString
  receivedAt: ISODateString
}
