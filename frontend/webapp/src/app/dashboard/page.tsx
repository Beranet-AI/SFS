"use client";

import { useLiveStatus } from "@/ui/hooks/useLiveStatus";

export default function DashboardPage() {
  // ⚠️ موقت: بعداً از selector یا route می‌آید
  const livestockId = "debug"; 

  const { data, loading } = useLiveStatus(livestockId);

  if (loading) {
    return <div style={{ padding: 16 }}>Loading live status…</div>;
  }

  if (!data || data.length === 0) {
    return (
      <div style={{ padding: 16 }}>
        <h2>Live Status</h2>
        <p style={{ color: "#999" }}>
          No live data received yet.
        </p>
      </div>
    );
  }

  return (
    <div style={{ padding: 16 }}>
      <h2>Live Status (SSE)</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: 12,
        }}
      >
        <thead>
          <tr style={{ background: "#222", color: "#fff" }}>
            <th style={{ padding: 8 }}>Timestamp</th>
            <th style={{ padding: 8 }}>Status</th>
            <th style={{ padding: 8 }}>Source</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #333" }}>
              <td style={{ padding: 8 }}>
                {new Date(row.timestamp).toLocaleString()}
              </td>
              <td style={{ padding: 8 }}>{row.state}</td>
              <td style={{ padding: 8 }}>{row.source}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Debug panel */}
      <details style={{ marginTop: 16 }}>
        <summary>Raw payload</summary>
        <pre style={{ background: "#111", color: "#0f0", padding: 12 }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      </details>
    </div>
  );
}
