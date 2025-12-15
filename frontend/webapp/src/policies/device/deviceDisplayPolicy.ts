import { DeviceKind } from '@/types/Device.dto'

export function deviceKindLabel(kind: DeviceKind): string {
  switch (kind) {
    case 'sensor':
      return 'Sensor'
    case 'camera':
      return 'Camera'
    case 'rfid':
      return 'RFID Reader'
    case 'motion_sensor':
      return 'Motion Sensor'
    case 'gateway':
      return 'Gateway'
    default:
      return 'Device'
  }
}

export function deviceStatusLabel(
  isActive: boolean,
): 'online' | 'offline' | 'inactive' {
  if (!isActive) return 'inactive'
  return 'online'
}
