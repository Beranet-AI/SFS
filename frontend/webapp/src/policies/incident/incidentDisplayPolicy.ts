import { IncidentSeverity, IncidentStatus } from '@/types/Incident.dto'

export function incidentSeverityDisplay(severity: IncidentSeverity) {
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

export function incidentStatusLabel(status: IncidentStatus): string {
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
