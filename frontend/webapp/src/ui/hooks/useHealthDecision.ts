"use client";

import { useState } from "react";
import { runHealthDecision } from "@/infrastructure/http/aiDecisionApi";

export function useHealthDecision() {
  const [loading, setLoading] = useState(false);

  async function run(livestockId: string) {
    setLoading(true);
    try {
      return await runHealthDecision(livestockId);
    } finally {
      setLoading(false);
    }
  }

  return { run, loading };
}
