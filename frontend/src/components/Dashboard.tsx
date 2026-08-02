import { Blueprint } from './Blueprint'

const kpis = [
  { label: 'Monthly sales', value: '—' },
  { label: 'Operating expenses', value: '—' },
  { label: 'Gross profit', value: '—' },
]

export function Dashboard() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 'var(--space-4)' }}>
        {kpis.map((kpi) => (
          <Blueprint key={kpi.label} className="card">
            <div className="card-kicker">{kpi.label}</div>
            <div className="card-title" style={{ fontSize: 26 }}>
              {kpi.value}
            </div>
          </Blueprint>
        ))}
      </div>

      <Blueprint className="card">
        <div className="card-title">Top customers</div>
        <table className="table">
          <thead>
            <tr>
              <th>Customer</th>
              <th style={{ textAlign: 'right' }}>Balance</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={2} className="text-muted">
                No data yet — connect the customers API.
              </td>
            </tr>
          </tbody>
        </table>
      </Blueprint>
    </div>
  )
}
