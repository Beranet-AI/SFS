// src/infrastructure/http/livestockApi.ts
import type { Livestock } from '@/types/Livestock.dto'
import { http } from './device'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

export function fetchLivestock(): Promise<Livestock[]> {
  return http<Livestock[]>(`${BASE}/livestock/`)
}
