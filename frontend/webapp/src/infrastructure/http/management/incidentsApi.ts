// src/infrastructure/http/management/incidentsApi.ts

import { httpClient } from '..//httpClient' // یا هر client مرکزی که داری
import type { Incident } from '@/types/Incident.dto' // یا مسیر دقیق DTOها

export const incidentsApi = {
  list(): Promise<Incident[]> {
    return httpClient.get('/api/management/incidents')
  },

  getById(id: string): Promise<Incident> {
    return httpClient.get(`/api/management/incidents/${id}`)
  },

  acknowledge(id: string): Promise<void> {
    return httpClient.post(`/api/management/incidents/${id}/acknowledge`)
  },

  resolve(id: string): Promise<void> {
    return httpClient.post(`/api/management/incidents/${id}/resolve`)
  },
}
