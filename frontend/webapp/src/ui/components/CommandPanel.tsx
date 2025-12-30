"use client";

import type { Command } from "@/domain/models/Command";
import { useTranslation } from "@/i18n/useTranslation";
import { formatDateTime } from "@/ui/utils/formatters";
import { EmptyState } from "@/ui/components/EmptyState";
import { Skeleton } from "@/ui/components/Skeleton";
import { CommandStatusBadge } from "@/ui/components/CommandStatusBadge";
import styles from "@/ui/styles/dashboard.module.css";

type CommandPanelProps = {
  commands: Command[];
  loading?: boolean;
};

export function CommandPanel({ commands, loading }: CommandPanelProps) {
  const { t, locale } = useTranslation();

  if (loading) {
    return (
      <div className={styles.liveStatusList}>
        <Skeleton />
        <Skeleton width="75%" />
      </div>
    );
  }

  if (commands.length === 0) {
    return <EmptyState message={t("commands.empty")} />;
  }

  return (
    <table className={styles.table}>
      <thead>
        <tr>
          <th>{t("commands.table.command")}</th>
          <th>{t("commands.table.target")}</th>
          <th>{t("commands.table.status")}</th>
          <th>{t("commands.table.issuedAt")}</th>
        </tr>
      </thead>
      <tbody>
        {commands.map((command) => (
          <tr key={command.id}>
            <td>{command.title}</td>
            <td>{command.targetLabel}</td>
            <td>
              <CommandStatusBadge status={command.status} />
            </td>
            <td>{formatDateTime(command.issuedAt, locale)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
