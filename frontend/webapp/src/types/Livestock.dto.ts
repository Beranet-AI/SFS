import { UUID, ISODateString } from './core.types'

/**
 * Livestock (Animal) Data Transfer Object
 * Source of truth: Backend
 */
export interface LivestockDTO {
  id: UUID

  /** Identity */
  tagNumber: string // ear tag or unique animal code
  name?: string // optional display name

  /** Classification */
  species: 'cow' | 'sheep' | 'goat' | 'other'
  breed?: string
  gender?: 'male' | 'female'

  /** Lifecycle */
  birthDate?: ISODateString
  isActive: boolean

  /** Location */
  farmId: UUID
  barnId?: UUID
  zoneId?: UUID

  /** Relations */
  primaryDeviceId?: UUID // main sensor or collar device

  /** Timestamps */
  createdAt: ISODateString
  updatedAt?: ISODateString
}
