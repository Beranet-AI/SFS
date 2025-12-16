// src/mappers/incident/incidentMapper.ts

import type { IncidentDTO } from '@/types/Incident.dto'
import type { IncidentVM } from '@/view-models/incident/IncidentVM'

/**
 * Translates IncidentDTO (API contract)
 * into IncidentVM (UI-friendly shape).
 *
 * No domain logic
 * No inference
 * No cross-service data
 */
export function mapIncidentToVM(dto: IncidentDTO): IncidentVM {
  return {
    id: dto.id,

    severity: dto.severity,
    status: dto.status,

    title: dto.title,
    message: dto.message,

    context: {
      farmId: dto.farm_id,
      barnId: dto.barn_id,
      zoneId: dto.zone_id,
      deviceId: dto.device_id,
    },

    metric: dto.metric,
    value: dto.value,

    createdAt: new Date(dto.created_at),
    updatedAt: new Date(dto.updated_at),
  }
}
