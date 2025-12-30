"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "sfs.seed-data";

export function useSeedPreference() {
  const [useSeed, setUseSeed] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored === "true") {
      setUseSeed(true);
    }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem(STORAGE_KEY, String(useSeed));
  }, [useSeed, hydrated]);

  return { useSeed, setUseSeed, hydrated };
}
