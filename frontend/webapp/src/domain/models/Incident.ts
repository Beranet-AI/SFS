import { IncidentSeverity, IncidentStatus } from "@/shared/enums";

export type Incident = {
  id: string;
  livestockId: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  source: string;
  description: string;
  createdAt: string;
  acknowledgedAt: string | null;
  resolvedAt: string | null;
};
