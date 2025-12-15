import { NextResponse } from 'next/server'

export interface Livestock {
  id: string
  farmId: string
  tagId: string
  species: 'cow' | 'sheep' | 'goat'
  status: 'healthy' | 'warning' | 'critical'
  createdAt: string
}

const LIVESTOCK: Livestock[] = [
  {
    id: 'cow-1',
    farmId: 'farm-1',
    tagId: 'RFID-0001',
    species: 'cow',
    status: 'healthy',
    createdAt: new Date().toISOString(),
  },
  {
    id: 'cow-2',
    farmId: 'farm-1',
    tagId: 'RFID-0002',
    species: 'cow',
    status: 'warning',
    createdAt: new Date().toISOString(),
  },
]

export async function GET() {
  return NextResponse.json(LIVESTOCK)
}
