export interface DeviceVM {
  id: string

  /** Display */
  displayName: string
  kindLabel: string
  locationLabel: string

  /** Status */
  isOnline: boolean
  statusLabel: 'online' | 'offline' | 'inactive'

  /** Optional UI helpers */
  primaryMetric?: string
}
