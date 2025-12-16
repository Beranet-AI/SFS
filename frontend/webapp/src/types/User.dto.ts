import { UUID } from './Core.types'

export type UserRole = 'admin' | 'vet' | 'operator' | 'viewer'

export interface CurrentUser {
  id: UUID
  role: UserRole
}
