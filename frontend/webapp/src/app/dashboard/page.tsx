"use client";

import { useEffect, useState } from "react";
import useSWR from "swr";

type SensorReading = {
  id: number;
  sensor: number;
  ts: string;
  value: number;
  quality: string;
  raw_payload?: any;
};

type ReadingsResponse = {
  readings: SensorReading[];
};

export default function DashboardPage() {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { data: alertsData } = useSWR("/api/alerts/active", async (url) => {
    const resp = await fetch(url);
    return resp.json();
  }, { refreshInterval: 5000 });

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const resp = await fetch("/api/readings");
        const data: ReadingsResponse = await resp.json();

        if (!resp.ok) {
          setError(JSON.stringify(data));
        } else {
          setReadings(data.readings || []);
        }
      } catch (e: any) {
        setError(String(e));
      } finally {
        setLoading(false);
      }
    }

    load();
    // هر ۵ ثانیه داده‌ها را ری‌فرش کن
    const timer = setInterval(load, 5000);
    return () => clearInterval(timer);
  }, []);

  // سنسورها: 1 = دما، 2 = آمونیاک
  const tempReadings = readings.filter((r) => r.sensor === 1);
  const ammoniaReadings = readings.filter((r) => r.sensor === 2);

  const lastTemp = tempReadings[0];
  const lastAmmonia = ammoniaReadings[0];
  const alertCount = alertsData?.alerts?.length ?? 0;

  return (
    <div style={{ padding: "24px", fontFamily: "system-ui" }}>
      <h1>SmartFarm Dashboard</h1>
      <div style={{ marginTop: "8px", marginBottom: "12px", display: "flex", gap: "12px", alignItems: "center" }}>
        <span style={{ padding: "6px 10px", borderRadius: "12px", background: alertCount > 0 ? "#7f1d1d" : "#1e3a8a", color: "white" }}>
          Active alerts: {alertCount}
        </span>
      </div>

      {loading && <p>Loading readings...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && (
        <>
          <section
            style={{
              display: "flex",
              gap: "16px",
              marginBottom: "24px",
              flexWrap: "wrap",
            }}
          >
            <div
              style={{
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid #ddd",
                minWidth: "220px",
              }}
            >
              <h2>Temperature (Sensor 1)</h2>
              {lastTemp ? (
                <>
                  <p style={{ fontSize: "32px", margin: 0 }}>
                    {lastTemp.value.toFixed(2)} °C
                  </p>
                  <small>
                    ts: {new Date(lastTemp.ts).toLocaleString()}
                  </small>
                </>
              ) : (
                <p>No temperature data.</p>
              )}
            </div>

            <div
              style={{
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid #ddd",
                minWidth: "220px",
              }}
            >
              <h2>Ammonia (Sensor 2)</h2>
              {lastAmmonia ? (
                <>
                  <p style={{ fontSize: "32px", margin: 0 }}>
                    {lastAmmonia.value.toFixed(2)} ppm
                  </p>
                  <small>
                    ts: {new Date(lastAmmonia.ts).toLocaleString()}
                  </small>
                </>
              ) : (
                <p>No ammonia data.</p>
              )}
            </div>
          </section>

          <section>
            <h2>Latest readings (raw)</h2>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: "14px",
              }}
            >
              <thead>
                <tr>
                  <th style={{ borderBottom: "1px solid #ccc" }}>ID</th>
                  <th style={{ borderBottom: "1px solid #ccc" }}>Sensor</th>
                  <th style={{ borderBottom: "1px solid #ccc" }}>Timestamp</th>
                  <th style={{ borderBottom: "1px solid #ccc" }}>Value</th>
                  <th style={{ borderBottom: "1px solid #ccc" }}>Quality</th>
                </tr>
              </thead>
              <tbody>
                {readings.map((r) => (
                  <tr key={r.id}>
                    <td style={{ borderBottom: "1px solid #eee" }}>{r.id}</td>
                    <td style={{ borderBottom: "1px solid #eee" }}>{r.sensor}</td>
                    <td style={{ borderBottom: "1px solid #eee" }}>
                      {new Date(r.ts).toLocaleString()}
                    </td>
                    <td style={{ borderBottom: "1px solid #eee" }}>{r.value}</td>
                    <td style={{ borderBottom: "1px solid #eee" }}>{r.quality}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </>
      )}
    </div>
  );
}
