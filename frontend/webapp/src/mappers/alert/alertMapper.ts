import { Alert } from '@/types/Alert.dto'
import { AlertVM } from '@/view-models/alert/AalertVM'
import { alertPolicy } from '@/policies/alert/alertPolicy'

export function mapAlertToVM(alert: Alert): AlertVM {
  const policy = alertPolicy(alert.severity)

  return {
    id: alert.id,

    title: alert.title,
    message: alert.message,

    severity: alert.severity,

    color: policy.color,
    icon: policy.icon,
    shouldPlaySound: policy.shouldPlaySound,
    isBlocking: policy.isBlocking,

    timestamp: alert.timestamp,
  }
}
