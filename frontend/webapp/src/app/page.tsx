'use client';

import React from "react";

type SingleReading = {
  id: number;
  sensor: number;
  ts: string;
  value: number;
  raw_payload: Record<string, unknown> | null;
  quality: string;
  created_at: string;
};

type LatestReadingsResponse = {
  temperature: SingleReading | null;
  ammonia: SingleReading | null;
};

async function getLatestReadings(): Promise<LatestReadingsResponse> {
  const baseUrl = process.env.NEXT_PUBLIC_DJANGO_API_BASE_URL;
  const token = process.env.NEXT_PUBLIC_DJANGO_API_TOKEN;

  if (!baseUrl || !token) {
    throw new Error(
      "DJANGO_API_BASE_URL یا DJANGO_API_TOKEN در .env.local تنظیم نشده است."
    );
  }

  const res = await fetch(`${baseUrl}/dashboard/latest-readings/`, {
    headers: {
      Authorization: `Token ${token}`,
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    console.error("Dashboard API error:", res.status, text);
    throw new Error(
      `Dashboard API error: ${res.status} - ${text.substring(0, 200)}`
    );
  }

  return await res.json();
}

export default async function HomePage() {
  let data: LatestReadingsResponse | null = null;
  let errorMessage: string | null = null;

  try {
    data = await getLatestReadings();
  } catch (err: any) {
    errorMessage = err?.message ?? "خطای نامشخص در دریافت داده‌ها";
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
            {/* Temperature Card */}
            <div className="rounded-xl border border-slate-700 bg-slate-900/60 p-4 shadow">
              <h2 className="text-lg font-medium mb-2">Temperature (دمــا)</h2>
              {data?.temperature ? (
                <>
                  <p className="text-3xl font-semibold">
                    {data.temperature.value.toFixed(2)}{" "}
                    <span className="text-base text-slate-400">°C</span>
                  </p>
                  <p className="mt-2 text-xs text-slate-400">
                    Sensor ID: {data.temperature.sensor} | کیفیت:{" "}
                    {data.temperature.quality}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    Last update:{" "}
                    {new Date(data.temperature.ts).toLocaleString()}
                  </p>
                </>
              ) : (
                <p className="text-sm text-slate-400">
                  هنوز داده‌ای برای دما ثبت نشده است.
                </p>
              )}
            </div>

            {/* Ammonia Card */}
            <div className="rounded-xl border border-slate-700 bg-slate-900/60 p-4 shadow">
              <h2 className="text-lg font-medium mb-2">Ammonia (آمونیاک)</h2>
              {data?.ammonia ? (
                <>
                  <p className="text-3xl font-semibold">
                    {data.ammonia.value.toFixed(2)}{" "}
                    <span className="text-base text-slate-400">ppm</span>
                  </p>
                  <p className="mt-2 text-xs text-slate-400">
                    Sensor ID: {data.ammonia.sensor} | کیفیت:{" "}
                    {data.ammonia.quality}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    Last update: {new Date(data.ammonia.ts).toLocaleString()}
                  </p>
                </>
              ) : (
                <p className="text-sm text-slate-400">
                  هنوز داده‌ای برای آمونیاک ثبت نشده است.
                </p>
              )}
            </div>
          </div>
        )}

        <p className="mt-4 text-center text-xs text-slate-500">
          داده‌ها از Django API: /api/v1/dashboard/latest-readings/ خوانده
          می‌شود.
        </p>
      </div>
    </main>
  );
}
