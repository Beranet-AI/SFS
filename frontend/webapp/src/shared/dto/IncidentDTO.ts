export type IncidentDTO = {
  id: string;
  livestock_id: string;
  severity: string;
  status: string;
  source: string;
  description: string;
  created_at: string;
  acknowledged_at: string | null;
  resolved_at: string | null;
};
