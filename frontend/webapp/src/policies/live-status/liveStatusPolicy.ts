import { Incident, LiveStatus, IncidentSeverity } from '@/types'

/* ===========================
   Live Status UI Policy
=========================== */

export function liveStatusPolicy(severity: IncidentSeverity) {
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
   Incident → Live Status Mapper
   (UI-only, NOT source of truth)
=========================== */

export function incidentToLiveStatus(event: Incident): LiveStatus {
  return {
    id: event.id, // Live Status id == Incident id (correlated)
    eventId: event.id,

    severity: event.severity,
    title: event.title,
    message: event.message,

    deviceId: event.deviceId,
    zoneId: event.zoneId,

    timestamp: event.createdAt,
  }
}
