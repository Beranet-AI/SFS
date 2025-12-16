import { UUID, ISODateString } from './Core.types'
import { IncidentSeverity } from './Incident.dto'

export interface LiveStatus {
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
