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

export type SensorSummary = {
  id: number;
  name: string;
  device_id: number | null;
  farm_id: number | null;
  barn_id: number | null;
  zone_id: number | null;
  sensor_type: {
    id: number;
    code: string;
    name: string;
    unit: string;
  };
};

export type ZoneNode = {
  id: number;
  name: string;
  code: string | null;
  description: string | null;
  sensor_count: number;
  sensors: SensorSummary[];
};

export type BarnNode = {
  id: number;
  name: string;
  code: string | null;
  description: string | null;
  sensor_count: number;
  sensors: SensorSummary[];
  zones: ZoneNode[];
};

export type FarmNode = {
  id: number;
  name: string;
  code: string | null;
  location?: string | null;
  sensor_count: number;
  sensors: SensorSummary[];
  barns: BarnNode[];
};

export type FarmHierarchyResponse = {
  farms: FarmNode[];
};

