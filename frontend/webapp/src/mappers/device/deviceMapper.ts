import { Device } from '@/types/Device.dto'
import { DeviceVM } from '@/view-models/device/DeviceVM'
import {
  deviceKindLabel,
  deviceStatusLabel,
} from '@/policies/device/deviceDisplayPolicy'

export function mapDeviceToVM(device: Device): DeviceVM {
  const locationLabel = device.zoneId
    ? `Zone ${device.zoneId}`
    : device.barnId
      ? `Barn ${device.barnId}`
      : 'Unassigned'

  return {
    id: device.id,
    displayName: device.name,
    kindLabel: deviceKindLabel(device.kind),
    locationLabel,
    isOnline: device.isActive,
    statusLabel: deviceStatusLabel(device.isActive),
    primaryMetric: device.metrics?.[0],
  }
}
