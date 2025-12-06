'use client'

import React from 'react'
import useSWR from 'swr'
import SensorCard from '../components/SensorCard'

type SingleReading = {
  id: number
  sensor: number
  ts: string
  value: number
  raw_payload: Record<string, unknown> | null
  quality: string
  created_at: string
}

type LatestReadingsResponse = Record<string, SingleReading | null>

const fetcher = async (url: string): Promise<LatestReadingsResponse> => {
  const baseUrl = process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL
  const token = process.env.NEXT_PUBLIC_DJANGO_API_TOKEN

  if (!baseUrl || !token) {
    throw new Error('NEXT_PUBLIC_DJANGO_API_BASE_URL یا NEXT_PUBLIC_DJANGO_API_TOKEN در .env.local تنظیم نشده است.')
  }

  const res = await fetch(`${baseUrl}${url}`, {
    headers: {
      Authorization: `Token ${token}`,
      Accept: 'application/json',
    },
    cache: 'no-store',
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Dashboard API error: ${res.status} - ${text.substring(0, 200)}`)
  }

  return res.json()
}

export default function HomePage() {
  const { data, error } = useSWR('/dashboard/latest-readings/', fetcher, {
    refreshInterval: 5000, // هر ۵ ثانیه یک بار اطلاعات را بگیرد
  })

  const defaultUnits: Record<string, string> = {
    temperature: '°C',
    ammonia: 'ppm',
  }
  const sensorLabelsFa: Record<string, string> = {
    temperature: 'دما',
    ammonia: 'آمونیاک',
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-4xl space-y-6">
        <h1 className="text-2xl md:text-3xl font-semibold text-center">
          SmartFarm – Live Telemetry Dashboard
        </h1>

        {error && (
          <div className="rounded-lg border border-red-500 bg-red-900/30 px-4 py-3 text-sm">
            <p className="font-semibold">خطا در ارتباط با Django API</p>
            <p className="mt-1 whitespace-pre-wrap break-words">{error.message}</p>
          </div>
        )}

        {!error && data && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data).map(([key, reading]) => (
              <SensorCard
                key={key}
                name={key.charAt(0).toUpperCase() + key.slice(1)}
                faLabel={sensorLabelsFa[key]}
                unit={defaultUnits[key]}
                reading={reading}
              />
            ))}
          </div>
        )}

        <p className="mt-4 text-center text-xs text-slate-500">
          داده‌ها از Django API: <code>/api/v1/dashboard/latest-readings/</code> خوانده می‌شود.
        </p>
      </div>
    </main>
  )
}
