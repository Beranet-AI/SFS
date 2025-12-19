import { HealthState } from "@/shared/enums";

export type Livestock = {
  id: string;
  tag: string;
  farmId: string;
  barn: string;
  zone: string;
  healthState: HealthState;
  healthConfidence: number;
  healthEvaluatedAt: string;
};
