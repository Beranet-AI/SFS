"use client";

import { useIncidents } from "@/ui/hooks/useIncidents";

export function IncidentsTable() {
  const { data, loading, ack, resolve } = useIncidents();

  if (loading) return <div>Loading incidents...</div>;

  return (
    <section>
      <h2>Incidents</h2>
      <table border={1} cellPadding={6} style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Livestock</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((i) => (
            <tr key={i.id}>
              <td>{i.id}</td>
              <td>{i.livestockId}</td>
              <td>{i.severity}</td>
              <td>{i.status}</td>
              <td style={{ display: "flex", gap: 8 }}>
                <button onClick={() => ack(i.id)}>Ack</button>
                <button onClick={() => resolve(i.id)}>Resolve</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
