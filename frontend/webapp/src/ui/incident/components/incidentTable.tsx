import type { IncidentVM } from '@/view-models/incident/IncidentVM'

interface Props {
  rows: IncidentVM[]
}

export function IncidentTable({ rows }: Props) {
  if (!rows.length) {
    return <div className="text-sm text-gray-500">No incidents</div>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse border text-sm">
        <thead>
          <tr className="bg-gray-50">
            <th className="border px-2 py-1 text-left">Time</th>
            <th className="border px-2 py-1 text-left">Severity</th>
            <th className="border px-2 py-1 text-left">Source</th>
            <th className="border px-2 py-1 text-left">Message</th>
            <th className="border px-2 py-1 text-left">Status</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="border px-2 py-1">{row.timestamp}</td>
              <td
                className={`border px-2 py-1 font-semibold ${
                  row.severityColor === 'red'
                    ? 'text-red-600'
                    : row.severityColor === 'yellow'
                      ? 'text-yellow-600'
                      : 'text-blue-600'
                }`}
              >
                {row.severityLabel}
              </td>
              <td className="border px-2 py-1">{row.sourceLabel}</td>
              <td className="border px-2 py-1">{row.message}</td>
              <td className="border px-2 py-1">{row.statusLabel}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
