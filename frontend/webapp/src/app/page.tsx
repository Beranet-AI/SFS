
// frontend/webapp/src/app/page.tsx

'use client'

import React from 'react'
import useSWR from 'swr'
import SensorCard from '../components/SensorCard'
import { sensorMetaMap } from '../lib/sensorMeta'

import type { SingleReading } from '../lib/types'

type LatestReadingsResponse = Record<string, SingleReading | null>

const ensureTrailingSlash = (base: string) => (base.endsWith('/') ? base : `${base}/`)

const joinPath = (prefix: string, endpoint: string) => {
  const cleanPrefix = prefix.replace(/^\/+|\/+$/g, '')
  const cleanEndpoint = endpoint.replace(/^\/+/, '')
  return cleanPrefix ? `${cleanPrefix}/${cleanEndpoint}` : cleanEndpoint
}

const fetcher = async (path: string): Promise<LatestReadingsResponse> => {
  const fastApiBase = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL
  const djangoApiBase = process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL
  const token = process.env.NEXT_PUBLIC_FASTAPI_TOKEN || process.env.NEXT_PUBLIC_DJANGO_API_TOKEN
  const apiPrefix = process.env.NEXT_PUBLIC_API_PREFIX || ''

  if (!fastApiBase && !djangoApiBase) {
    throw new Error(
      'حداقل یکی از متغیرهای NEXT_PUBLIC_FASTAPI_BASE_URL یا NEXT_PUBLIC_DJANGO_API_BASE_URL در .env.local تنظیم نشده است.'
    )
  }

  const base = ensureTrailingSlash(fastApiBase || djangoApiBase!)
  const targetPath = joinPath(apiPrefix, path)
  const target = new URL(targetPath, base)

  const headers: HeadersInit = {
    Accept: 'application/json',
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const res = await fetch(target.toString(), {
    headers,
    cache: 'no-store',
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Dashboard API error: ${res.status} - ${text.substring(0, 200)} (URL: ${target})`)
  }

  return res.json()
}

export default function HomePage() {
  const { data, error } = useSWR('dashboard/latest-readings/', fetcher, {
    refreshInterval: 5000,
  })

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-6xl space-y-6">
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(data).map(([key, reading]) => {
              const meta = sensorMetaMap[key] || { name: key }
              return (
                <SensorCard
                  key={key}
                  name={meta.name}
                  faLabel={meta.faLabel}
                  unit={meta.unit}
                  icon={meta.icon}
                  color={meta.color}
                  reading={reading}
                />
              )
            })}
          </div>
        )}

        <p className="mt-4 text-center text-xs text-slate-500">
          داده‌ها از FastAPI (یا به صورت مستقیم از Django) از مسیر <code>dashboard/latest-readings/</code> روی <code>BASE_URL</code>
          واکشی می‌شود؛ در صورت نیاز می‌توانید پیشوندی مثل <code>api/v1</code> را در متغیر
          <code>NEXT_PUBLIC_API_PREFIX</code> تنظیم کنید تا مسیر کامل مانند <code>/api/v1/dashboard/latest-readings/</code>
          ساخته شود.
        </p>
      </div>
    </main>
  )
}
