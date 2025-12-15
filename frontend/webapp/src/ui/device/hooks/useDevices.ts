'use client'

import { useEffect, useMemo, useState } from 'react'

import { fetchDevices } from '@/infrastructure/http/deviceApi'
import { mapDeviceToVM } from '@/mappers/device/deviceMapper'

import type { Device } from '@/types/Device.dto'
import type { DeviceVM } from '@/view-models/device/DeviceVM'

export function useDevices(): {
  devices: DeviceVM[]
  loading: boolean
} {
  const [data, setData] = useState<Device[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true

    async function load() {
      setLoading(true)
      try {
        const result = await fetchDevices()
        if (mounted) {
          setData(result)
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    load()

    return () => {
      mounted = false
    }
  }, [])

  const devices = useMemo(() => {
    return data.map(mapDeviceToVM)
  }, [data])

  return { devices, loading }
}
