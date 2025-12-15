import type { Device } from '@/types/Device.dto'
import { http } from './event'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

/**
 * Fetch all devices visible to current user
 */
export async function fetchDevices(): Promise<Device[]> {
  try {
    return await http<Device[]>(`${BASE}/devices/`)
  } catch (err) {
    console.error('fetchDevices failed:', err)
    return [] // 👈 بسیار مهم
  }
}

/**
 * Fetch single device (optional)
 */
export function fetchDeviceById(id: string): Promise<Device> {
  return http<Device>(`${BASE}/devices/${id}/`)
}
