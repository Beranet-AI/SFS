'use client'

import { AlertIndicator } from '@/ui/alert/components/AlertIndicator'
import { TelemetryChart } from '@/ui/telemetry/charts/TelemetryChart'
import { DeviceList } from '@/ui/device/components/DeviceList'
import { LivestockList } from '@/ui/livestock/components/LivestockList'
import { EventTable } from '@/ui/event/components/EventTable'

import { useAlerts } from '@/ui/alert/hooks/useAlerts'
import { useTelemetry } from '@/ui/telemetry/hooks/useTelemetry'
import { useDevices } from '@/ui/device/hooks/useDevices'
import { useLivestock } from '@/ui/livestock/hooks/useLivestock'
import { useEvents } from '@/ui/event/hooks/useEvents'

export default function Dashboard() {
  const { alerts } = useAlerts()
  const { series } = useTelemetry()
  const { devices } = useDevices()
  const { livestock } = useLivestock()
  const { events } = useEvents()

  return (
    <main className="space-y-6 p-6">
      {/* Alerts */}
      <AlertIndicator alerts={alerts} />

      {/* Charts */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TelemetryChart series={series} />
      </section>

      {/* Lists */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DeviceList devices={devices} />
        <LivestockList livestock={livestock} />
      </section>

      {/* Events */}
      <section>
        <EventTable rows={events} />
      </section>
    </main>
  )
}
