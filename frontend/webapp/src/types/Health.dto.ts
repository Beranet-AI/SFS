import { ISODateString } from './Core.types'

export interface HealthStatus {
  service: string
  status: 'ok' | 'degraded' | 'down'
  timestamp: ISODateString
}
