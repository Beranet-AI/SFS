"use client";

import { useLivestock } from "@/ui/hooks/useLivestock";
import { useTranslation } from "@/i18n/useTranslation";

export function LivestockTable() {
  const { data, loading } = useLivestock();
  const { t } = useTranslation();

  if (loading) return <div>{t("livestock.loading")}</div>;

  return (
    <section>
      <h2>{t("livestock.title")}</h2>
      <table border={1} cellPadding={6} style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>{t("livestock.id")}</th>
            <th>{t("livestock.tag")}</th>
            <th>{t("livestock.location")}</th>
            <th>{t("livestock.health")}</th>
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
