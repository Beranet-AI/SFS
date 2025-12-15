import type { Incident } from '@/types/incidentDto'
import type { IncidentVM } from '@/view-models/incident/IncidentVM'

/**
 * Maps domain Incident to IncidentVM for UI layer
 */
export function mapIncidentToVM(event: Incident): IncidentVM {
  return {
    id: event.id,
    title: event.type,
    description: event.description ?? '—',
    timestamp: event.timestamp,
    severity: event.severity ?? 'info',
  }
}
