import { UUID, ISODateString } from './core.types'
import { IncidentSeverity } from './incident.dto'

export interface LiveStatusDTO {
  id: UUID

  severity: IncidentSeverity

  title: string
  message: string

  eventId: UUID

  deviceId?: UUID
  zoneId?: UUID

  payload?: {
    metric: string
    value: number
  }

  timestamp: ISODateString
}
