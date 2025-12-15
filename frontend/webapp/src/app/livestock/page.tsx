'use client'

import { useEffect, useState } from 'react'

interface Livestock {
  id: string
  farmId: string
  tagId: string
  species: 'cow' | 'sheep' | 'goat'
  status: 'healthy' | 'warning' | 'critical'
  createdAt: string
}

export default function LivestockPage() {
  const [animals, setAnimals] = useState<Livestock[]>([])

  useEffect(() => {
    fetch('/api/livestock')
      .then((r) => r.json() as Promise<Livestock[]>)
      .then(setAnimals)
  }, [])

  return (
    <main className="space-y-6">
      <h1 className="text-2xl font-bold">Livestock</h1>

      <ul className="space-y-2">
        {animals.map((a) => (
          <li key={a.id} className="rounded border p-3">
            <div className="font-medium">{a.tagId}</div>
            <div className="text-sm text-gray-500">
              {a.species} – {a.status}
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}
