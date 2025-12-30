export type TelemetryPoint = {
  timestamp: string;
  value: number;
};

export type TelemetrySeries = {
  metric: string;
  unit: string;
  points: TelemetryPoint[];
};
