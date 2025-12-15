import { UUID, ISODateString } from './Core.types'
import { EventSeverity } from './Event.dto'

export interface Alert {
  id: UUID

  severity: EventSeverity

  title: string
  message: string

  eventId: UUID

  deviceId?: UUID
  zoneId?: UUID

  timestamp: ISODateString
}
