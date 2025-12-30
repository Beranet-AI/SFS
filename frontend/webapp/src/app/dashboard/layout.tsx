"use client";

import { AppSidebar } from "@/ui/components/AppSidebar";
import { AppTopbar } from "@/ui/components/AppTopbar";
import styles from "@/ui/styles/dashboard.module.css";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.dashboardLayout}>
      <AppSidebar />
      <div className={styles.dashboardMain}>
        <AppTopbar />
        <main className={styles.dashboardContent}>{children}</main>
      </div>
    </div>
  );
}
