import { UserRole } from '@/types/User.dto'

export function userRoleLabel(role: UserRole): string {
  switch (role) {
    case 'admin':
      return 'Administrator'
    case 'vet':
      return 'Veterinarian'
    case 'operator':
      return 'Operator'
    case 'viewer':
    default:
      return 'Viewer'
  }
}

export function userRoleCapabilities(role: UserRole) {
  return {
    canViewDashboard: true,
    canViewLivestock: role !== 'viewer',
    canViewIncidents: role !== 'viewer',

    canAcknowledgeIncidents: role === 'admin' || role === 'operator',
    canResolveIncidents: role === 'admin',
  }
}
