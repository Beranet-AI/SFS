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
    canViewEvents: role !== 'viewer',

    canAcknowledgeAlerts: role === 'admin' || role === 'operator',
    canResolveEvents: role === 'admin',
  }
}
