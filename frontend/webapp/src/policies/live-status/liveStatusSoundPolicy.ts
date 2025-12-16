import { LiveStatus } from '@/types/LiveStatus.dto'

export function shouldPlaySound(status: LiveStatus): boolean {
  return status.severity === 'critical'
}
