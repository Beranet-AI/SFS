"use client";

import { IncidentSeverity, IncidentStatus } from "@/shared/enums";
import type { Farm } from "@/domain/models/Farm";
import type { Livestock } from "@/domain/models/Livestock";
import type { Incident } from "@/domain/models/Incident";

const FOUR_HOURS = 4 * 60 * 60 * 1000;

export function useDashboardKpis({
  farms,
  livestock,
  incidents,
}: {
  farms: Farm[];
  livestock: Livestock[];
  incidents: Incident[];
}) {
  const activeFarms = farms.filter((farm) => farm.status === "active").length;
  const onlineLivestock = livestock.filter((animal) => {
    const lastCheck = new Date(animal.healthEvaluatedAt).getTime();
    return Date.now() - lastCheck < FOUR_HOURS;
  }).length;
  const activeAlerts = incidents.filter(
    (incident) => incident.status !== IncidentStatus.RESOLVED
  ).length;

  const severityPenalty = incidents.reduce((score, incident) => {
    if (incident.status === IncidentStatus.RESOLVED) return score;
    switch (incident.severity) {
      case IncidentSeverity.CRITICAL:
        return score + 18;
      case IncidentSeverity.HIGH:
        return score + 12;
      case IncidentSeverity.MEDIUM:
        return score + 6;
      default:
        return score + 3;
    }
  }, 0);

  const systemHealth = Math.max(60, 100 - severityPenalty);

  return {
    activeFarms,
    onlineLivestock,
    activeAlerts,
    systemHealth,
  };
}
