import { useMemo } from 'react'
import { mapLivestockToVM } from '@/mappers/livestock/livestockMapper'
import { useDevices } from '@/ui/device/hooks/useDevices'
import { useIncidents } from '@/ui/incident/hooks/useIncidents'

export function useLivestock() {
  const { devices } = useDevices()
  const { incidents } = useIncidents()

  const livestock = useMemo(
    () => mapLivestockToVM({ devices, events: incidents }),
    [devices, incidents],
  )

  return {
    livestock,
  }
}
