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

export type AlertRule = {
  id: number;
  name: string;
  description?: string | null;
  farm: number;
  sensor: number | null;
  sensor_type: number | null;
  threshold_value: number;
  operator: 'greater_than' | 'less_than';
  severity: 'info' | 'warn' | 'critical';
  is_active: boolean;
  created_at: string;
};

export type AlertLog = {
  id: number;
  rule: number | null;
  farm: number;
  barn: number | null;
  zone: number | null;
  sensor: number | null;
  severity: 'info' | 'warn' | 'critical';
  reading_value: number | null;
  message: string;
  status: 'open' | 'ack' | 'resolved';
  raised_at: string;
  resolved_at: string | null;
  extra_data: Record<string, unknown> | null;
  created_at: string;
};

