"use client";

import { useLiveStatus } from "@/ui/hooks/useLiveStatus";
import { useHealthDecision } from "@/ui/hooks/useHealthDecision";
import { useTranslation } from "@/i18n/useTranslation";
import { useState } from "react";

export function LiveStatusPanel() {
  const [livestockId, setLivestockId] = useState("1");
  const { data, loading } = useLiveStatus(livestockId);
  const { run, loading: decisionLoading } = useHealthDecision();
  const { t } = useTranslation();

  return (
    <section>
      <h2>{t("livestatus.title")}</h2>

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input
          value={livestockId}
          onChange={(e) => setLivestockId(e.target.value)}
          placeholder={t("livestatus.inputPlaceholder")}
        />
        <button
          onClick={() => run(livestockId)}
          disabled={decisionLoading}
        >
          {t("livestatus.runDecision")}
        </button>
      </div>

      {loading ? (
        <div>{t("livestatus.loading")}</div>
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
