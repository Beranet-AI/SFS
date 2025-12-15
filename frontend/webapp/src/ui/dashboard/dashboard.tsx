'use client'

import { LiveStatusIndicator } from '@/ui/live-status/components/liveStatusIndicator'
import { TelemetryChart } from '@/ui/telemetry/charts/TelemetryChart'
import { DeviceList } from '@/ui/device/components/DeviceList'
import { LivestockList } from '@/ui/livestock/components/LivestockList'
import { IncidentTable } from '@/ui/incident/components/incidentTable'

import { useLiveStatuses } from '@/ui/live-status/hooks/useLiveStatuses'
import { useTelemetry } from '@/ui/telemetry/hooks/useTelemetry'
import { useDevices } from '@/ui/device/hooks/useDevices'
import { useLivestock } from '@/ui/livestock/hooks/useLivestock'
import { useIncidents } from '@/ui/incident/hooks/useIncidents'

export default function Dashboard() {
  const statuses = useLiveStatuses()
  const { series } = useTelemetry()
  const { devices } = useDevices()
  const { livestock } = useLivestock()
  const { incidents } = useIncidents()

  return (
    <main className="space-y-6 p-6">
      {/* Live Status */}
      <LiveStatusIndicator statuses={statuses} />

      {/* Charts */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TelemetryChart series={series} />
      </section>

      {/* Lists */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DeviceList devices={devices} />
        <LivestockList livestock={livestock} />
      </section>

      {/* Incidents */}
      <section>
        <IncidentTable rows={incidents} />
      </section>
    </main>
  )
}
