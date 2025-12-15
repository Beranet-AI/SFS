export interface userVM {
  id: string

  /** Display */
  role: 'admin' | 'vet' | 'operator' | 'viewer'
  roleLabel: string

  /** UI capabilities (NOT security) */
  canViewDashboard: boolean
  canViewLivestock: boolean
  canViewIncidents: boolean

  canAcknowledgeIncidents: boolean
  canResolveIncidents: boolean
}
