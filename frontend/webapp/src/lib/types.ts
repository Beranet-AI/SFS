export type SingleReading = {
  id: number;
  sensor: number;
  ts: string;
  value: number;
  raw_payload: Record<string, unknown> | null;
  quality: string;
  created_at: string;
};

export type LatestReadingsResponse = Record<string, SingleReading | null>;

export type HistoricalReading = {
  ts: string;
  value: number;
  quality: string;
};

export type SensorMeta = {
  name: string;
  faLabel?: string;
  unit?: string;
  color?: string;
  icon?: string;
};

