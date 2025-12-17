import { UUID } from './core.types'

export type UserRole = 'admin' | 'vet' | 'operator' | 'viewer'

export interface CurrentUserDTO {
  id: UUID
  role: UserRole
}
