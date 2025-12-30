import { CommandStatus } from "@/shared/enums";

export type Command = {
  id: string;
  title: string;
  targetId: string;
  targetLabel: string;
  status: CommandStatus;
  issuedAt: string;
  executedAt?: string | null;
  source: string;
};
