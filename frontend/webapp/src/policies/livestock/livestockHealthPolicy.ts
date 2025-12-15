export function livestockHealthLabel(
  status: 'healthy' | 'warning' | 'critical',
): string {
  switch (status) {
    case 'critical':
      return 'Critical'
    case 'warning':
      return 'Needs Attention'
    case 'healthy':
    default:
      return 'Healthy'
  }
}
