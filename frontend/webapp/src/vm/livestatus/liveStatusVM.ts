export interface LiveStatusVM {
  id: string

  title: string
  message: string

  severity: 'info' | 'warning' | 'critical'

  /** UI concerns */
  color: 'blue' | 'yellow' | 'red'
  icon: 'info' | 'warning' | 'error'

  shouldPlaySound: boolean
  isBlocking: boolean

  timestamp: string
}
