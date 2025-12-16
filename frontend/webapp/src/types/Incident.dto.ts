// src/types/Incident.dto.ts

/**
 * Mirror of backend EventSerializer (Management owned)
 * This is a pure API contract DTO.
 * NO UI fields
 * NO derived fields
 */
export interface IncidentDTO {
  id: string

  severity: string // as provided by backend
  status: string // lifecycle state (OPEN, ACK, RESOLVED, ...)

  title: string
  message: string

  // contextual references (read-only)
  farm_id: string | null
  barn_id: string | null
  zone_id: string | null
  device_id: string | null

  // snapshot context coming from management
  metric: string | null
  value: number | string | null

  created_at: string // ISO datetime
  updated_at: string // ISO datetime
}
