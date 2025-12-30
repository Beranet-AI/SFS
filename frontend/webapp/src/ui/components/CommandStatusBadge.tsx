"use client";

import { CommandStatus } from "@/shared/enums";
import { useTranslation } from "@/i18n/useTranslation";
import { StatusBadge } from "@/ui/components/StatusBadge";

const statusTone: Record<CommandStatus, "success" | "warning" | "danger"> = {
  [CommandStatus.QUEUED]: "warning",
  [CommandStatus.SENT]: "warning",
  [CommandStatus.EXECUTED]: "success",
  [CommandStatus.FAILED]: "danger",
};

export function CommandStatusBadge({ status }: { status: CommandStatus }) {
  const { t } = useTranslation();
  return (
    <StatusBadge
      tone={statusTone[status]}
      label={t(`commands.status.${status}` as never)}
    />
  );
}
