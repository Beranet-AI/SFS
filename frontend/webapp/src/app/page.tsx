
// frontend/webapp/src/app/page.tsx

'use client'

import React from 'react'
import useSWR from 'swr'
import SensorCard from '../components/SensorCard'
import { sensorMetaMap } from '../lib/sensorMeta'

import type { FarmHierarchyResponse, FarmNode, SingleReading } from '../lib/types'

type LatestReadingsResponse = Record<string, SingleReading | null>
type LatestReadingsKey = [path: string, sensorTypesOverride?: string | null]

type ApiConfigOptions = {
  preferDjango?: boolean
}

type ApiConfig = {
  base: string
  apiPrefix: string
  headers: HeadersInit
  buildUrl: (endpoint: string) => URL
}

const ensureTrailingSlash = (base: string) => (base.endsWith('/') ? base : `${base}/`)

const joinPath = (prefix: string, endpoint: string) => {
  const cleanPrefix = prefix.replace(/^\/+|\/+$/g, '')
  const cleanEndpoint = endpoint.replace(/^\/+/, '')
  return cleanPrefix ? `${cleanPrefix}/${cleanEndpoint}` : cleanEndpoint
}

const buildApiConfig = (options: ApiConfigOptions = {}): ApiConfig => {
  const fastApiBase = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL
  const djangoApiBase = process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL
  const token = process.env.NEXT_PUBLIC_FASTAPI_TOKEN || process.env.NEXT_PUBLIC_DJANGO_API_TOKEN
  const apiPrefix = process.env.NEXT_PUBLIC_API_PREFIX || ''
  const preferDjango = options.preferDjango ?? false

  const primaryBase = preferDjango ? djangoApiBase : fastApiBase
  const fallbackBase = preferDjango ? fastApiBase : djangoApiBase
  const resolvedBase = primaryBase || fallbackBase

  if (!resolvedBase) {
    throw new Error(
      'حداقل یکی از متغیرهای NEXT_PUBLIC_FASTAPI_BASE_URL یا NEXT_PUBLIC_DJANGO_API_BASE_URL در .env.local تنظیم نشده است.'
    )
  }

  const base = ensureTrailingSlash(resolvedBase)
  const headers: HeadersInit = {
    Accept: 'application/json',
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const buildUrl = (endpoint: string) => new URL(joinPath(apiPrefix, endpoint), base)

  return { base, apiPrefix, headers, buildUrl }
}

const sensorTypesCache: { value: string | null } = { value: null }

const resolveSensorTypes = async (
  config: ApiConfig,
  configuredSensorTypes?: string
): Promise<string> => {
  const explicit = (configuredSensorTypes || '')
    .split(',')
    .map((c) => c.trim())
    .filter(Boolean)

  if (explicit.length) {
    return explicit.join(',')
  }

  if (sensorTypesCache.value) {
    return sensorTypesCache.value
  }

  const sensorTypesUrl = config.buildUrl('sensor-types/')
  const res = await fetch(sensorTypesUrl.toString(), {
    headers: config.headers,
    cache: 'no-store',
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Sensor types fetch failed: ${res.status} - ${text.substring(0, 200)} (URL: ${sensorTypesUrl})`)
  }

  const payload = await res.json()
  const codes = Array.isArray(payload)
    ? payload
        .map((item) => (item && typeof item === 'object' ? (item as { code?: string }).code : null))
        .filter((code): code is string => Boolean(code))
    : []

  if (!codes.length) {
    throw new Error('Sensor types endpoint returned no codes. لطفاً مطمئن شوید SensorType در Django تعریف شده است.')
  }

  sensorTypesCache.value = codes.join(',')
  return sensorTypesCache.value
}

const latestReadingsFetcher = async ([
  path,
  sensorTypesOverride,
]: LatestReadingsKey): Promise<LatestReadingsResponse> => {
  const config = buildApiConfig()
  const configuredSensorTypes = process.env.NEXT_PUBLIC_SENSOR_TYPES

  const target = config.buildUrl(path)

  const sensorTypes =
    sensorTypesOverride || (await resolveSensorTypes(config, configuredSensorTypes))

  // کنترل می‌کنیم که لیست سنسورها دقیقاً با کدهای تعریف‌شده در Django هماهنگ باشد
  target.searchParams.set('sensor_types', sensorTypes)

  const res = await fetch(target.toString(), {
    headers: config.headers,
    cache: 'no-store',
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Dashboard API error: ${res.status} - ${text.substring(0, 200)} (URL: ${target})`)
  }

  return res.json()
}

const hierarchyFetcher = async (path: string): Promise<FarmHierarchyResponse> => {
  const config = buildApiConfig({ preferDjango: true })
  const target = config.buildUrl(path)

  const res = await fetch(target.toString(), {
    headers: config.headers,
    cache: 'no-store',
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Farm hierarchy error: ${res.status} - ${text.substring(0, 200)} (URL: ${target})`)
  }

  return res.json()
}

export default function HomePage() {
  const { data: hierarchy, error: hierarchyError } = useSWR<FarmHierarchyResponse>(
    'dashboard/farm-hierarchy/',
    hierarchyFetcher,
    {
      refreshInterval: 30000,
    }
  )

  const farms = hierarchy?.farms ?? []
  const [selectedFarmId, setSelectedFarmId] = React.useState<number | null>(null)
  const [selectedBarnId, setSelectedBarnId] = React.useState<number | null>(null)
  const [selectedZoneId, setSelectedZoneId] = React.useState<number | null>(null)

  React.useEffect(() => {
    if (farms.length && !selectedFarmId) {
      setSelectedFarmId(farms[0].id)
    }
  }, [farms, selectedFarmId])

  const selectedFarm: FarmNode | null = React.useMemo(
    () => farms.find((farm) => farm.id === selectedFarmId) ?? null,
    [farms, selectedFarmId]
  )

  const selectedFarmHasSensors = React.useMemo(() => {
    if (!selectedFarm) return false

    const farmLevel = selectedFarm.sensors?.length ?? 0
    const barns = selectedFarm.barns ?? []

    const barnLevel = barns.some((barn) => {
      const direct = barn.sensors?.length ?? 0
      const zones = barn.zones ?? []
      const zoneSensors = zones.some((zone) => (zone.sensors?.length ?? 0) > 0)
      return direct > 0 || zoneSensors
    })

    return farmLevel > 0 || barnLevel
  }, [selectedFarm])

  React.useEffect(() => {
    if (selectedFarm?.barns?.length) {
      if (!selectedBarnId || !selectedFarm.barns.some((barn) => barn.id === selectedBarnId)) {
        setSelectedBarnId(selectedFarm.barns[0].id)
      }
    } else {
      setSelectedBarnId(null)
    }
  }, [selectedBarnId, selectedFarm])

  React.useEffect(() => {
    if (!selectedFarmHasSensors) {
      setSelectedBarnId(null)
      setSelectedZoneId(null)
    }
  }, [selectedFarmHasSensors])

  const selectedBarn = React.useMemo(
    () => selectedFarm?.barns.find((barn) => barn.id === selectedBarnId) ?? null,
    [selectedBarnId, selectedFarm]
  )

  React.useEffect(() => {
    if (selectedBarn?.zones?.length) {
      if (!selectedZoneId || !selectedBarn.zones.some((zone) => zone.id === selectedZoneId)) {
        setSelectedZoneId(selectedBarn.zones[0].id)
      }
    } else {
      setSelectedZoneId(null)
    }
  }, [selectedBarn, selectedZoneId])

  const selectedZone = React.useMemo(
    () => selectedBarn?.zones.find((zone) => zone.id === selectedZoneId) ?? null,
    [selectedBarn, selectedZoneId]
  )

  const selectedZoneHasSensors = React.useMemo(() => {
    if (!selectedZone) return false
    return (selectedZone.sensors?.length ?? 0) > 0
  }, [selectedZone])

  const selectedZoneSensorTypes = React.useMemo(() => {
    if (!selectedZone?.sensors?.length) return []

    const codes = selectedZone.sensors
      .map((sensor) => sensor.sensor_type.code)
      .filter(Boolean)

    return Array.from(new Set(codes))
  }, [selectedZone])

  const { data, error } = useSWR(
    selectedZoneSensorTypes.length
      ? (['dashboard/latest-readings/', selectedZoneSensorTypes.join(',')] as LatestReadingsKey)
      : null,
    latestReadingsFetcher,
    {
      refreshInterval: 5000,
      keepPreviousData: false,
      revalidateOnFocus: false,
    }
  )

  const renderSensors = (sensors: FarmNode['sensors']) => {
    if (!sensors?.length) {
      return <span className="text-xs text-slate-500">سنسوری ثبت نشده</span>
    }

    return (
      <div className="flex flex-wrap gap-2 mt-2">
        {sensors.map((sensor) => (
          <span
            key={`sensor-${sensor.id}`}
            className="rounded-full bg-slate-800/70 px-3 py-1 text-xs text-slate-200 border border-slate-700"
          >
            {sensor.name} <span className="text-slate-400">({sensor.sensor_type.code})</span>
          </span>
        ))}
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-6xl space-y-6">
        <h1 className="text-2xl md:text-3xl font-semibold text-center">
          SmartFarm – Live Telemetry Dashboard
        </h1>

        <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
            <div>
              <h2 className="text-xl font-semibold">ساختار مزرعه → بارن → زون</h2>
              <p className="text-sm text-slate-400">
                ابتدا مزرعه را انتخاب کنید تا بارن‌ها، زون‌ها و سنسورهای هر بخش نمایش داده شود.
              </p>
            </div>
            <span className="text-xs text-slate-500">به‌روزرسانی هر ۳۰ ثانیه از مسیر dashboard/farm-hierarchy/</span>
          </div>

          {hierarchyError && (
            <div className="mt-3 rounded-lg border border-red-500 bg-red-900/30 px-4 py-3 text-sm">
              <p className="font-semibold">خطا در واکشی ساختار مزارع</p>
              <p className="mt-1 whitespace-pre-wrap break-words">{hierarchyError.message}</p>
            </div>
          )}

          {!hierarchy && !hierarchyError && (
            <p className="mt-3 text-sm text-slate-400">در حال بارگذاری ساختار مزارع...</p>
          )}

          {hierarchy?.farms?.length ? (
            <div className="mt-4 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {farms.map((farm) => (
                  <button
                    key={`farm-${farm.id}`}
                    type="button"
                    onClick={() => {
                      setSelectedFarmId(farm.id)
                      setSelectedBarnId(null)
                      setSelectedZoneId(null)
                    }}
                    className={`rounded-lg border px-4 py-3 text-left transition hover:border-slate-400/80 hover:shadow ${
                      selectedFarmId === farm.id ? 'border-emerald-400/80 bg-emerald-950/30' : 'border-slate-800 bg-slate-950/40'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <p className="text-base font-semibold">{farm.name}</p>
                        {farm.location && <p className="text-xs text-slate-500">{farm.location}</p>}
                      </div>
                      <span className="text-xs text-slate-400">سنسورها: {farm.sensor_count}</span>
                    </div>
                    <p className="mt-1 text-xs text-slate-500">تعداد بارن‌ها: {farm.barns.length}</p>
                  </button>
                ))}
              </div>

              {selectedFarm && (
                <div className="space-y-3 rounded-lg border border-slate-800/80 bg-slate-950/40 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="text-lg font-semibold">بارن‌های {selectedFarm.name}</h3>
                    <span className="text-xs text-slate-400">تعداد سنسورها: {selectedFarm.sensor_count}</span>
                  </div>

                  {selectedFarm.sensors.length > 0 && (
                    <div>
                      <p className="text-xs text-slate-400">سنسورهای ثبت‌شده برای خود مزرعه (بدون بارن/زون):</p>
                      {renderSensors(selectedFarm.sensors)}
                    </div>
                  )}

                  {selectedFarm.barns.length ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {selectedFarm.barns.map((barn) => (
                        <button
                          key={`barn-${barn.id}`}
                          type="button"
                          onClick={() => {
                            setSelectedBarnId(barn.id)
                            setSelectedZoneId(null)
                          }}
                          className={`rounded-lg border px-3 py-3 text-left transition hover:border-slate-400/80 hover:shadow ${
                            selectedBarnId === barn.id ? 'border-sky-400/80 bg-sky-950/40' : 'border-slate-800 bg-slate-900/40'
                          }`}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <p className="text-base font-medium">{barn.name}</p>
                            <span className="text-xs text-slate-400">سنسورها: {barn.sensor_count}</span>
                          </div>
                          <p className="mt-1 text-xs text-slate-500">تعداد زون‌ها: {barn.zones.length}</p>
                          {barn.description && <p className="mt-1 text-xs text-slate-500">{barn.description}</p>}
                          {renderSensors(barn.sensors)}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-500">برای این مزرعه هنوز بارنی ثبت نشده است.</p>
                  )}

                  {selectedBarn && (
                    <div className="space-y-3 rounded-lg border border-slate-800 bg-slate-900/40 p-4">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <h4 className="text-base font-semibold">زون‌های {selectedBarn.name}</h4>
                        <span className="text-xs text-slate-400">سنسورها: {selectedBarn.sensor_count}</span>
                      </div>

                      {selectedBarn.sensors.length > 0 && (
                        <div>
                          <p className="text-xs text-slate-400">سنسورهای همین بارن:</p>
                          {renderSensors(selectedBarn.sensors)}
                        </div>
                      )}

                      {selectedBarn.zones.length ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {selectedBarn.zones.map((zone) => (
                            <button
                              key={`zone-${zone.id}`}
                              type="button"
                              onClick={() => setSelectedZoneId(zone.id)}
                              className={`w-full rounded-lg border p-3 text-left transition hover:border-emerald-400/80 hover:shadow ${
                                selectedZoneId === zone.id
                                  ? 'border-emerald-400/80 bg-emerald-950/40'
                                  : 'border-slate-800 bg-slate-950/60'
                              }`}
                            >
                              <div className="flex items-center justify-between gap-2">
                                <p className="text-sm font-semibold">{zone.name}</p>
                                <span className="text-xs text-slate-400">سنسورها: {zone.sensor_count}</span>
                              </div>
                              {zone.code && <p className="text-xs text-slate-500">کد: {zone.code}</p>}
                              {renderSensors(zone.sensors)}
                            </button>
                          ))}
                        </div>
                      ) : (
                        <p className="text-sm text-slate-500">زون ثبت نشده است؛ سنسورها در سطح خود بارن هستند.</p>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            !hierarchyError && <p className="mt-3 text-sm text-slate-500">هنوز مزرعه‌ای ثبت نشده است.</p>
          )}
        </section>

        {error && (
          <div className="rounded-lg border border-red-500 bg-red-900/30 px-4 py-3 text-sm">
            <p className="font-semibold">خطا در ارتباط با Django API</p>
            <p className="mt-1 whitespace-pre-wrap break-words">{error.message}</p>
          </div>
        )}

        {!error && selectedFarm && !selectedFarmHasSensors && (
          <div className="rounded-lg border border-slate-800 bg-slate-900/60 px-4 py-3 text-sm text-slate-200">
            برای مزرعه انتخاب‌شده هیچ سنسوری ثبت نشده است؛ لطفاً مزرعه دیگری را انتخاب کنید.
          </div>
        )}

        {!error && selectedFarm && selectedFarmHasSensors && !selectedZone && (
          <div className="rounded-lg border border-amber-500/40 bg-amber-900/20 px-4 py-3 text-sm text-amber-100">
            لطفاً یک زون را انتخاب کنید تا مقادیر سنسورها نمایش داده شود.
          </div>
        )}

        {!error && selectedZone && !selectedZoneHasSensors && (
          <div className="rounded-lg border border-slate-700 bg-slate-900/50 px-4 py-3 text-sm text-slate-200">
            برای زون انتخاب‌شده هنوز سنسوری ثبت نشده است.
          </div>
        )}

        {!error &&
          selectedFarm &&
          selectedFarmHasSensors &&
          selectedZone &&
          selectedZoneHasSensors &&
          selectedZoneSensorTypes.length > 0 &&
          data && (
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
          واکشی می‌شود. اگر <code>NEXT_PUBLIC_SENSOR_TYPES</code> را ست نکنید، فرانت‌اند ابتدا <code>sensor-types/</code> را می‌خواند و
          به صورت خودکار کد سنسورها را از Django استخراج می‌کند؛ در غیر این صورت مقدار متغیر را (مثلاً <code>temp_sensor,ammonia</code>)
          استفاده می‌کند. در صورت نیاز می‌توانید پیشوندی مثل <code>api/v1</code> را هم در <code>NEXT_PUBLIC_API_PREFIX</code> بگذارید تا
          مسیر کامل مانند <code>/api/v1/dashboard/latest-readings/?sensor_types=...</code> ساخته شود. اکنون کارت‌ها فقط پس از انتخاب
          زون (و وجود سنسور در آن زون) نمایش داده می‌شوند. برای ساختار مزرعه نیز از <code>dashboard/farm-hierarchy/</code> استفاده
          می‌شود و انتخاب مزرعه/بارن/زون در بالا مسیر نظارت را شفاف می‌کند.
        </p>
      </div>
    </main>
  )
}
