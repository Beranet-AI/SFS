import type { IncidentDTO } from "@/shared/dto";
import { IncidentSeverity, IncidentStatus } from "@/shared/enums";
import type { Incident } from "@/domain/models/Incident";

export function mapIncident(dto: IncidentDTO): Incident {
  return {
    id: dto.id,
    livestockId: dto.livestock_id,
    severity: dto.severity as IncidentSeverity,
    status: dto.status as IncidentStatus,
    source: dto.source,
    description: dto.description,
    createdAt: dto.created_at,
    acknowledgedAt: dto.acknowledged_at,
    resolvedAt: dto.resolved_at,
  };
}
