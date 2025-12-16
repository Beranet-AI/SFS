import { LiveStatus } from '@/types/LiveStatus.dto'
import { LiveStatusVM } from '@/view-models/live-status/liveStatusVM'
import { liveStatusPolicy } from '@/policies/live-status/liveStatusPolicy'

export function mapLiveStatusToVM(status: LiveStatus): LiveStatusVM {
  const policy = liveStatusPolicy(status.severity)

  return {
    id: status.id,

    title: status.title,
    message: status.message,

    severity: status.severity,

    color: policy.color,
    icon: policy.icon,
    shouldPlaySound: policy.shouldPlaySound,
    isBlocking: policy.isBlocking,

    timestamp: status.timestamp,
  }
}
