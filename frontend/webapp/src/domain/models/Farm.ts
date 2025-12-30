export type Farm = {
  id: string;
  name: string;
  location: string;
  status: "active" | "maintenance" | "offline";
  livestockCount: number;
  devicesOnline: number;
};
