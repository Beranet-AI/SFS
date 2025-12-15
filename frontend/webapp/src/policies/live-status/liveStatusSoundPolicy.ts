import { LiveStatus } from '@/types/liveStatusDto'

export function shouldPlaySound(status: LiveStatus): boolean {
  return status.severity === 'critical'
}
