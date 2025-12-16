// src/ui/dashboard/dashboard.tsx
'use client'

import { useIncidents } from '@/ui/incident/hooks/useIncidents'

export default function Dashboard() {
  const { incidents, loading, error } = useIncidents()

  if (loading) return <div>Loading incidents...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h2>Active Incidents</h2>
      <ul>
        {incidents.map((incident) => (
          <li key={incident.id}>
            {incident.title} [{incident.severity}]
          </li>
        ))}
      </ul>
    </div>
  )
}
