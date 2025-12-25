"use client";

import { useLiveStatus } from "@/hooks/useLiveStatus";

export default function DashboardPage() {
  const { data, loading } = useLiveStatus(undefined); // یا livestockId مشخص

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: 16 }}>
      <h2>LiveStatus (SSE)</h2>
      <pre style={{ background: "#111", color: "#0f0", padding: 12 }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
