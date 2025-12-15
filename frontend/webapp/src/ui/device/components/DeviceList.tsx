import type { deviceVM } from '@/view-models/device/DeviceVM'

interface Props {
  devices: deviceVM[]
}

export function DeviceList({ devices }: Props) {
  if (!devices.length) {
    return <div className="text-sm text-gray-500">No devices</div>
  }

  return (
    <div className="space-y-2">
      {devices.map((device) => (
        <div
          key={device.id}
          className="flex items-center justify-between rounded border p-3"
        >
          <div>
            <div className="font-medium">{device.displayName}</div>
            <div className="text-xs text-gray-500">
              {device.kindLabel} · {device.locationLabel}
            </div>
          </div>

          <span
            className={`text-xs font-semibold ${
              device.isOnline ? 'text-green-600' : 'text-gray-400'
            }`}
          >
            {device.statusLabel}
          </span>
        </div>
      ))}
    </div>
  )
}
