import { Event, Alert, EventSeverity } from '@/types'

/* ===========================
   Alert UI Policy
=========================== */

export function alertPolicy(severity: EventSeverity) {
  switch (severity) {
    case 'critical':
      return {
        color: 'red',
        icon: 'error',
        shouldPlaySound: true,
        isBlocking: true,
      }

    case 'warning':
      return {
        color: 'yellow',
        icon: 'warning',
        shouldPlaySound: false,
        isBlocking: false,
      }

    case 'info':
    default:
      return {
        color: 'blue',
        icon: 'info',
        shouldPlaySound: false,
        isBlocking: false,
      }
  }
}

/* ===========================
   Event → Alert Mapper
   (UI-only, NOT source of truth)
=========================== */

export function eventToAlert(event: Event): Alert {
  return {
    id: event.id, // Alert id == Event id (correlated)
    eventId: event.id,

    severity: event.severity,
    title: event.title,
    message: event.message,

    deviceId: event.deviceId,
    zoneId: event.zoneId,

    timestamp: event.createdAt,
  }
}
