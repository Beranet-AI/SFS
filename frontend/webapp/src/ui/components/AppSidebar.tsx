"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "@/i18n/useTranslation";
import styles from "@/ui/styles/dashboard.module.css";

const navItems = [
  { href: "/dashboard", key: "nav.overview" },
  { href: "/dashboard#livestatus", key: "nav.liveStatus" },
  { href: "/dashboard#telemetry", key: "nav.telemetry" },
  { href: "/dashboard#health", key: "nav.health" },
  { href: "/dashboard#commands", key: "nav.commands" },
  { href: "/dashboard#incidents", key: "nav.incidents" },
];

export function AppSidebar() {
  const { t } = useTranslation();
  const pathname = usePathname();

  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarBrand}>
        <span className={styles.sidebarTitle}>{t("layout.brand")}</span>
        <span className={styles.sidebarSubtitle}>{t("layout.brandSubtitle")}</span>
      </div>
      <nav className={styles.navList}>
        {navItems.map((item) => {
          const isActive = pathname === item.href.split("#")[0];
          return (
            <Link
              key={item.key}
              href={item.href}
              className={`${styles.navItem} ${
                isActive ? styles.navItemActive : ""
              }`}
            >
              <span>{t(item.key as never)}</span>
              <span>↗</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
