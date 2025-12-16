// src/mappers/incident/incidentMapper.ts

import type { IncidentDto } from '@/types'
import type { IncidentViewModel } from '@/view-models/incident/IncidentViewModel'

function severityToColor(severity: IncidentDto['severity']): string {
  switch (severity) {
    case 'CRITICAL':
      return 'red'
    case 'HIGH':
      return 'orange'
    case 'MEDIUM':
      return 'yellow'
    default:
      return 'gray'
  }
}

export function mapIncidentToViewModel(dto: IncidentDto): IncidentViewModel {
  return {
    id: dto.id,
    title: dto.title ?? 'Incident',
    state: dto.state,
    severity: dto.severity,
    color: severityToColor(dto.severity),
    isActionable: dto.state !== 'RESOLVED',
  }
}
