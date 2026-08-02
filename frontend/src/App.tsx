import { useState } from 'react'
import { Blueprint } from './components/Blueprint'
import { Sidebar, type NavKey } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'

const titles: Record<NavKey, string> = {
  dashboard: 'Dashboard',
  customers: 'Customers',
  suppliers: 'Suppliers',
  pricing: 'Pricing',
  sales: 'Sales',
  purchases: 'Purchases',
  cash: 'Cash In/Out',
  production: 'Production',
  settings: 'Settings',
}

function App() {
  const [active, setActive] = useState<NavKey>('dashboard')

  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100vh',
        minHeight: 700,
        background: 'var(--color-bg)',
        color: 'var(--color-text)',
        fontFamily: 'var(--font-body)',
        overflow: 'hidden',
      }}
    >
      <Sidebar active={active} onSelect={setActive} />

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Blueprint
          as="nav"
          className="nav"
          style={{ flex: 'none', margin: 'var(--space-3) var(--space-3) 0' }}
        >
          <div className="nav-brand">{titles[active]}</div>
        </Blueprint>

        <div style={{ flex: 1, overflowY: 'auto', padding: 'var(--space-4)' }}>
          {active === 'dashboard' ? (
            <Dashboard />
          ) : (
            <Blueprint className="card">
              <div className="card-title">{titles[active]}</div>
              <p className="card-body">Not built yet — coming as the domain models land.</p>
            </Blueprint>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
