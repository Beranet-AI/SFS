import { HealthState, IncidentSeverity, IncidentStatus, CommandStatus } from "@/shared/enums";
import type { Livestock } from "@/domain/models/Livestock";
import type { Incident } from "@/domain/models/Incident";
import type { LiveStatus } from "@/domain/models/LiveStatus";
import type { Farm } from "@/domain/models/Farm";
import type { TelemetrySeries } from "@/domain/models/Telemetry";
import type { Command } from "@/domain/models/Command";
import type { HealthRisk } from "@/domain/models/HealthRisk";

const now = Date.now();

const hoursAgo = (hours: number) => new Date(now - hours * 60 * 60 * 1000).toISOString();

export const seedFarms: Farm[] = [
  {
    id: "farm-01",
    name: "Shiraz North Farm",
    location: "Shiraz, Iran",
    status: "active",
    livestockCount: 240,
    devicesOnline: 56,
  },
  {
    id: "farm-02",
    name: "Qazvin Greenhouse",
    location: "Qazvin, Iran",
    status: "active",
    livestockCount: 120,
    devicesOnline: 34,
  },
  {
    id: "farm-03",
    name: "Tabriz Research Hub",
    location: "Tabriz, Iran",
    status: "maintenance",
    livestockCount: 80,
    devicesOnline: 12,
  },
];

export const seedLivestock: Livestock[] = [
  {
    id: "ls-001",
    tag: "LS-2041",
    farmId: "farm-01",
    barn: "Barn A",
    zone: "Zone 3",
    healthState: HealthState.HEALTHY,
    healthConfidence: 0.92,
    healthEvaluatedAt: hoursAgo(1),
  },
  {
    id: "ls-002",
    tag: "LS-2088",
    farmId: "farm-01",
    barn: "Barn B",
    zone: "Zone 1",
    healthState: HealthState.AT_RISK,
    healthConfidence: 0.74,
    healthEvaluatedAt: hoursAgo(2),
  },
  {
    id: "ls-003",
    tag: "LS-3120",
    farmId: "farm-02",
    barn: "Barn C",
    zone: "Zone 2",
    healthState: HealthState.SICK,
    healthConfidence: 0.61,
    healthEvaluatedAt: hoursAgo(3),
  },
  {
    id: "ls-004",
    tag: "LS-4189",
    farmId: "farm-03",
    barn: "Barn A",
    zone: "Zone 5",
    healthState: HealthState.CRITICAL,
    healthConfidence: 0.48,
    healthEvaluatedAt: hoursAgo(6),
  },
];

export const seedLiveStatus: LiveStatus[] = [
  {
    deviceId: "dev-45",
    livestockId: "ls-001",
    metric: "Temperature",
    value: 38.2,
    recordedAt: hoursAgo(0.5),
  },
  {
    deviceId: "dev-45",
    livestockId: "ls-001",
    metric: "Heart Rate",
    value: 82,
    recordedAt: hoursAgo(0.6),
  },
  {
    deviceId: "dev-52",
    livestockId: "ls-002",
    metric: "Humidity",
    value: 56,
    recordedAt: hoursAgo(0.4),
  },
  {
    deviceId: "dev-73",
    livestockId: "ls-003",
    metric: "Feed Intake",
    value: 2.3,
    recordedAt: hoursAgo(0.9),
  },
];

export const seedIncidents: Incident[] = [
  {
    id: "inc-1092",
    livestockId: "LS-2088",
    severity: IncidentSeverity.HIGH,
    status: IncidentStatus.ACKNOWLEDGED,
    source: "health-monitor",
    description: "Abnormal respiration detected in Zone 1",
    createdAt: hoursAgo(4),
    acknowledgedAt: hoursAgo(3.5),
    resolvedAt: null,
  },
  {
    id: "inc-1093",
    livestockId: "LS-3120",
    severity: IncidentSeverity.CRITICAL,
    status: IncidentStatus.OPEN,
    source: "iot-gateway",
    description: "Telemetry loss detected for 12 minutes",
    createdAt: hoursAgo(1.5),
    acknowledgedAt: null,
    resolvedAt: null,
  },
  {
    id: "inc-1094",
    livestockId: "LS-2041",
    severity: IncidentSeverity.MEDIUM,
    status: IncidentStatus.RESOLVED,
    source: "ai-decision",
    description: "Temperature spike normalized after cooling command",
    createdAt: hoursAgo(7),
    acknowledgedAt: hoursAgo(6.5),
    resolvedAt: hoursAgo(6),
  },
];

export const seedTelemetrySeries: TelemetrySeries[] = [
  {
    metric: "Temperature",
    unit: "°C",
    points: Array.from({ length: 12 }, (_, index) => ({
      timestamp: hoursAgo(12 - index),
      value: 37.5 + Math.sin(index / 2) * 0.6 + index * 0.03,
    })),
  },
  {
    metric: "Humidity",
    unit: "%",
    points: Array.from({ length: 12 }, (_, index) => ({
      timestamp: hoursAgo(12 - index),
      value: 54 + Math.cos(index / 2) * 4 + index * 0.2,
    })),
  },
  {
    metric: "Activity",
    unit: "steps/hr",
    points: Array.from({ length: 12 }, (_, index) => ({
      timestamp: hoursAgo(12 - index),
      value: 120 + Math.sin(index) * 18 + index * 3,
    })),
  },
];

export const seedHealthRisks: HealthRisk[] = [
  {
    id: "risk-001",
    livestockId: "ls-002",
    livestockTag: "LS-2088",
    riskLevel: IncidentSeverity.HIGH,
    score: 78,
    status: HealthState.AT_RISK,
    lastEvaluatedAt: hoursAgo(2),
  },
  {
    id: "risk-002",
    livestockId: "ls-003",
    livestockTag: "LS-3120",
    riskLevel: IncidentSeverity.CRITICAL,
    score: 92,
    status: HealthState.SICK,
    lastEvaluatedAt: hoursAgo(1),
  },
  {
    id: "risk-003",
    livestockId: "ls-004",
    livestockTag: "LS-4189",
    riskLevel: IncidentSeverity.MEDIUM,
    score: 64,
    status: HealthState.AT_RISK,
    lastEvaluatedAt: hoursAgo(3),
  },
];

export const seedCommands: Command[] = [
  {
    id: "cmd-88",
    title: "Adjust Ventilation",
    targetId: "farm-01",
    targetLabel: "Shiraz North Farm",
    status: CommandStatus.EXECUTED,
    issuedAt: hoursAgo(2),
    executedAt: hoursAgo(1.8),
    source: "automation-engine",
  },
  {
    id: "cmd-89",
    title: "Increase Cooling",
    targetId: "ls-003",
    targetLabel: "LS-3120",
    status: CommandStatus.SENT,
    issuedAt: hoursAgo(0.7),
    executedAt: null,
    source: "ai-decision",
  },
  {
    id: "cmd-90",
    title: "Schedule Vet Visit",
    targetId: "ls-004",
    targetLabel: "LS-4189",
    status: CommandStatus.QUEUED,
    issuedAt: hoursAgo(0.4),
    executedAt: null,
    source: "care-team",
  },
];
