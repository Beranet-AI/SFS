
//frontend/webapp/src/components/SensorChart.tsx


'use client';

import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function SensorChart({ sensorId, color = '#38bdf8' }: { sensorId: number, color?: string }) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetch(`/api/readings?sensor_id=${sensorId}&limit=20`);
        const result = await res.json();
        setData(result.readings);
      } catch (e) {
        console.error('Error loading chart data:', e);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [sensorId]);

  if (loading) return <p className="text-xs text-slate-500">Loading chart...</p>;
  if (!data || data.length === 0) {
  return <p className="text-xs text-slate-500">No chart data</p>;
}


  return (
    <ResponsiveContainer width="100%" height={100}>
      <LineChart data={data}>
        <XAxis dataKey="ts" hide />
        <YAxis hide domain={['dataMin', 'dataMax']} />
        <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
        <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
