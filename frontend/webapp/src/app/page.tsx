'use client'

import React, { useEffect, useState } from 'react'

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

export default function HomePage() {
  const [data, setData] = useState<LatestReadingsResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    const fetchReadings = async () => {
      const baseUrl = process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL
      const token = process.env.NEXT_PUBLIC_DJANGO_API_TOKEN

      if (!baseUrl || !token) {
        setErrorMessage('NEXT_PUBLIC_DJANGO_API_BASE_URL یا NEXT_PUBLIC_DJANGO_API_TOKEN در .env.local تنظیم نشده است.')
        return
      }

      try {
        const res = await fetch(`${baseUrl}/dashboard/latest-readings/`, {
          headers: {
            Authorization: `Token ${token}`,
            Accept: 'application/json',
          },
          cache: 'no-store',
        })

        if (!res.ok) {
          const text = await res.text()
          setErrorMessage(`Dashboard API error: ${res.status} - ${text.substring(0, 200)}`)
        } else {
          const result = (await res.json()) as LatestReadingsResponse
          setData(result)
        }
      } catch (err: any) {
        setErrorMessage(err?.message ?? 'خطای نامشخص در دریافت داده‌ها')
      }
    }

    fetchReadings()
  }, [])

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
      <div className="w-full max-w-3xl space-y-6">
        <h1 className="text-2xl md:text-3xl font-semibold text-center">
          SmartFarm – Live Telemetry Dashboard
        </h1>

        {errorMessage && (
          <div className="rounded-lg border border-red-500 bg-red-900/30 px-4 py-3 text-sm">
            <p className="font-semibold">خطا در ارتباط با Django API</p>
            <p className="mt-1 whitespace-pre-wrap break-words">
              {errorMessage}
            </p>
          </div>
        )}

        {!errorMessage && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data &&
              Object.entries(data).map(([key, reading]) => {
                const labelEn = key.charAt(0).toUpperCase() + key.slice(1)
                const labelFa = sensorLabelsFa[key] ?? ''
                const unit = defaultUnits[key] ?? ''
                return (
                  <div key={key} className="rounded-xl border border-slate-700 bg-slate-900/60 p-4 shadow">
                    <h2 className="text-lg font-medium mb-2">
                      {labelEn} {labelFa && `(${labelFa})`}
                    </h2>
                    {reading ? (
                      <>
                        <p className="text-3xl font-semibold">
                          {reading.value.toFixed(2)}{' '}
                          <span className="text-base text-slate-400">{unit}</span>
                        </p>
                        <p className="mt-2 text-xs text-slate-400">
                          Sensor ID: {reading.sensor} | کیفیت: {reading.quality}
                        </p>
                        <p className="mt-1 text-xs text-slate-500">
                          Last update: {new Date(reading.ts).toLocaleString()}
                        </p>
                      </>
                    ) : (
                      <p className="text-sm text-slate-400">
                        {`هنوز داده‌ای برای ${labelFa || labelEn} ثبت نشده است.`}
                      </p>
                    )}
                  </div>
                )
              })}
          </div>
        )}

        <p className="mt-4 text-center text-xs text-slate-500">
          داده‌ها از Django API: /api/v1/dashboard/latest-readings/ خوانده می‌شود.
        </p>
      </div>
    </main>
  )
}
