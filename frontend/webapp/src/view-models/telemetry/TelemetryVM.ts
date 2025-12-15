export interface TelemetryPointVM {
  x: string // formatted time for chart axis
  y: number
}

export interface TelemetryVM {
  metric: string

  /** Display */
  metricLabel: string
  unit: string

  /** Chart-ready data */
  points: TelemetryPointVM[]

  /** Summary */
  min?: number
  max?: number
  latest?: number

  /** UI hints */
  hasAnomaly?: boolean
}
