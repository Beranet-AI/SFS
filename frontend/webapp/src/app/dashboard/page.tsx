import { LiveStatusPanel } from "@/ui/components/LiveStatusPanel";
import { IncidentsTable } from "@/ui/components/IncidentsTable";
import { LivestockTable } from "@/ui/components/LivestockTable";

export default function DashboardPage() {
  return (
    <main style={{ padding: 16, display: "grid", gap: 16 }}>
      <h1>Dashboard</h1>
      <LiveStatusPanel />
      <IncidentsTable />
      <LivestockTable />
    </main>
  );
}
