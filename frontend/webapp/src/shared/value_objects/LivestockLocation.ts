import { FarmId } from "@/shared/ids";

export type LivestockLocation = {
  farmId: FarmId;
  barn: string;
  zone: string;
};
