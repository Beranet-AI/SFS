// src/policies/incident/incidentDisplayPolicy.ts

import type { IncidentVM } from '@/view-models/incident/IncidentVM';

/**
 * UI display helpers for Incident
 * No domain logic allowed here
 */

export function getIncidentSeverityColor(vm: IncidentVM): string {
  switch (vm.severity) {
    case 'CRITICAL':
      return 'red';
    case 'HIGH':
      return 'orange';
    case 'MEDIUM':
      return 'yellow';
    default:
      return 'gray';
  }
}

export function getIncidentStatusLabel(vm: IncidentVM): string {
  switch (vm.status) {
    case 'OPEN':
      return 'Open';
    case 'ACK':
    case 'ACKNOWLEDGED':
      return 'Acknowledged';
    case 'RESOLVED':
      return 'Resolved';
    default:
      return vm.status;
  }
}

export function formatIncidentMetric(vm: IncidentVM): string | null {
  if (!vm.metric || vm.value === null || vm.value === undefined) {
    return null;
  }

  return `${vm.metric}: ${vm.value}`;
}
