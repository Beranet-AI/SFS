"use client";

import { useLivestock } from "@/ui/hooks/useLivestock";

export function LivestockTable() {
  const { data, loading } = useLivestock();

  if (loading) return <div>Loading livestock...</div>;

  return (
    <section>
      <h2>Livestock</h2>
      <table border={1} cellPadding={6} style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Tag</th>
            <th>Location</th>
            <th>Health</th>
          </tr>
        </thead>
        <tbody>
          {data.map((l) => (
            <tr key={l.id}>
              <td>{l.id}</td>
              <td>{l.tag}</td>
              <td>{l.farmId} / {l.barn} / {l.zone}</td>
              <td>{l.healthState} ({l.healthConfidence})</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
