// src/view-models/incident/IncidentVM.ts

export interface IncidentVM {
  id: string;

  severity: string;
  status: string;

  title: string;
  message: string;

  context: {
    farmId: string | null;
    barnId: string | null;
    zoneId: string | null;
    deviceId: string | null;
  };

  metric: string | null;
  value: number | string | null;

  createdAt: Date;
  updatedAt: Date;
}
