"use client";

import { useLiveStatus } from "@/ui/hooks/useLiveStatus";
import { useHealthDecision } from "@/ui/hooks/useHealthDecision";
import { useState } from "react";

export function LiveStatusPanel() {
  const [livestockId, setLivestockId] = useState("1");
  const { data, loading } = useLiveStatus(livestockId);
  const { run, loading: decisionLoading } = useHealthDecision();

  return (
    <section>
      <h2>Live Status</h2>

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input
          value={livestockId}
          onChange={(e) => setLivestockId(e.target.value)}
          placeholder="Livestock ID"
        />
        <button
          onClick={() => run(livestockId)}
          disabled={decisionLoading}
        >
          Run AI Decision
        </button>
      </div>

      {loading ? (
        <div>Loading livestatus...</div>
      ) : (
        <ul>
          {data.map((s, idx) => (
            <li key={idx}>
              {s.metric}: {s.value} ({s.recordedAt})
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
