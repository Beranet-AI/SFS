import { IncidentSeverity, HealthState } from "@/shared/enums";

export type HealthRisk = {
  id: string;
  livestockId: string;
  livestockTag: string;
  riskLevel: IncidentSeverity;
  score: number;
  status: HealthState;
  lastEvaluatedAt: string;
};
