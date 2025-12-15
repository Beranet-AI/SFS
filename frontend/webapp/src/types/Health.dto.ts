import { ISODateString } from './core.types'

export interface HealthStatus {
  service: string
  status: 'ok' | 'degraded' | 'down'
  timestamp: ISODateString
}
