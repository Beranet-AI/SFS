import { Alert } from '@/types/Alert.dto'

export function shouldPlaySound(alert: Alert): boolean {
  return alert.severity === 'critical'
}
