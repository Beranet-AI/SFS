"use client";

import { useEffect, useState } from "react";
import type { Command } from "@/domain/models/Command";
import { seedCommands } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseCommandsOptions = {
  useSeed?: boolean;
};

export function useCommands(options: UseCommandsOptions = {}) {
  const [data, setData] = useState<Command[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("seed");
  const { useSeed } = options;

  useEffect(() => {
    async function load() {
      setLoading(true);
      if (useSeed) {
        setData(seedCommands);
        setSource("seed");
        setLoading(false);
        return;
      }

      // TODO: Replace seedCommands with real management API once /commands endpoint is available.
      setData(seedCommands);
      setSource("seed");
      setLoading(false);
    }

    load();
  }, [useSeed]);

  return { data, loading, source };
}
