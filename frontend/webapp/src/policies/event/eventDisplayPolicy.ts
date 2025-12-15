import { EventSeverity, EventStatus } from '@/types/Event.dto'

export function eventSeverityDisplay(severity: EventSeverity) {
  switch (severity) {
    case 'critical':
      return { label: 'Critical', color: 'red' }
    case 'warning':
      return { label: 'Warning', color: 'yellow' }
    case 'info':
    default:
      return { label: 'Info', color: 'blue' }
  }
}

export function eventStatusLabel(status: EventStatus): string {
  switch (status) {
    case 'ack':
      return 'Acknowledged'
    case 'resolved':
      return 'Resolved'
    case 'raised':
    default:
      return 'Raised'
  }
}
