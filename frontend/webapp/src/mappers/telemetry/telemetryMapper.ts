import type { TelemetryReading } from '@/types/Telemetry.dto'
import type {
  TelemetryVM,
  TelemetryPointVM,
} from '@/view-models/telemetry/telemetryVM'
import { telemetryMetricLabel } from '@/policies/telemetry/telemetryDisplayPolicy'

export function mapTelemetryToVM(
  metric: string,
  unit: string,
  readings: TelemetryReading[] = [], // ✅ default
): TelemetryVM {
  const safeReadings = readings ?? [] // double safety

  const points: TelemetryPointVM[] = safeReadings
    .slice()
    .sort(
      (a, b) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    )
    .map((r) => ({
      x: new Date(r.timestamp).toLocaleTimeString(),
      y: r.value,
    }))

  const values = safeReadings.map((r) => r.value)

  return {
    metric,
    metricLabel: telemetryMetricLabel(metric),
    unit,

    points,

    min: values.length ? Math.min(...values) : undefined,
    max: values.length ? Math.max(...values) : undefined,
    latest: values.length ? values[values.length - 1] : undefined,
  }
}
