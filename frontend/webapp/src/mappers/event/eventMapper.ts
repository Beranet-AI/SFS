import type { Event } from '@/types/Event.dto'
import type { EventVM } from '@/view-models/event/EventVM'

/**
 * Maps domain Event to EventVM for UI layer
 */
export function mapEventToVM(event: Event): EventVM {
  return {
    id: event.id,
    title: event.type,
    description: event.description ?? '—',
    timestamp: event.timestamp,
    severity: event.severity ?? 'info',
  }
}
