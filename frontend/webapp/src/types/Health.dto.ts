import { ISODateString } from './core.types'

export interface HealthStatusDTO {
  service: string
  status: 'ok' | 'degraded' | 'down'
  timestamp: ISODateString
}
