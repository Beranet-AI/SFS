import { SensorMetric } from '@/types/Device.dto'

export function telemetryMetricLabel(metric: SensorMetric): string {
  switch (metric) {
    case 'temperature':
      return 'Temperature'
    case 'humidity':
      return 'Humidity'
    case 'ammonia':
      return 'Ammonia'
    case 'heart_rate':
      return 'Heart Rate'
    case 'movement_score':
      return 'Activity'
    case 'weight':
      return 'Weight'
    case 'milk_yield':
      return 'Milk Yield'
    default:
      return metric
  }
}
