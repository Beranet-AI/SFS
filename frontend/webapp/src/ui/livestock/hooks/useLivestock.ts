import { useMemo } from 'react'
import { mapLivestockToVM } from '@/mappers/livestock/livestockMapper'
import { useDevices } from '@/ui/device/hooks/useDevices'
import { useEvents } from '@/ui/event/hooks/useEvents'

export function useLivestock() {
  const { devices } = useDevices()
  const { events } = useEvents()

  const livestock = useMemo(
    () => mapLivestockToVM({ devices, events }),
    [devices, events],
  )

  return {
    livestock,
  }
}
