import { UUID } from './core.types'

export type UserRole = 'admin' | 'vet' | 'operator' | 'viewer'

export interface CurrentUser {
  id: UUID
  role: UserRole
}
