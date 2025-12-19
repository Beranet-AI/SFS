"use client";

import { useIncidents } from "@/ui/hooks/useIncidents";
import { useTranslation } from "@/i18n/useTranslation";

export function IncidentsTable() {
  const { data, loading, ack, resolve } = useIncidents();
  const { t } = useTranslation();

  if (loading) return <div>{t("incidents.loading")}</div>;

  return (
    <section>
      <h2>{t("incidents.title")}</h2>
      <table border={1} cellPadding={6} style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>{t("incidents.id")}</th>
            <th>{t("incidents.livestock")}</th>
            <th>{t("incidents.severity")}</th>
            <th>{t("incidents.status")}</th>
            <th>{t("incidents.actions")}</th>
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
                <button onClick={() => ack(i.id)}>{t("incidents.ack")}</button>
                <button onClick={() => resolve(i.id)}>{t("incidents.resolve")}</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
