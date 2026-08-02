import {
  LayoutGrid,
  Users,
  Truck,
  Tag,
  BarChart3,
  Package,
  Wallet,
  Factory,
  Settings,
} from 'lucide-react'
import { Blueprint } from './Blueprint'

export type NavKey =
  | 'dashboard'
  | 'customers'
  | 'suppliers'
  | 'pricing'
  | 'sales'
  | 'purchases'
  | 'cash'
  | 'production'
  | 'settings'

const managementItems: { key: NavKey; label: string; icon: typeof LayoutGrid }[] = [
  { key: 'dashboard', label: 'Dashboard', icon: LayoutGrid },
  { key: 'customers', label: 'Customers', icon: Users },
  { key: 'suppliers', label: 'Suppliers', icon: Truck },
  { key: 'pricing', label: 'Pricing', icon: Tag },
]

const accountingItems: { key: NavKey; label: string; icon: typeof LayoutGrid }[] = [
  { key: 'sales', label: 'Sales', icon: BarChart3 },
  { key: 'purchases', label: 'Purchases', icon: Package },
  { key: 'cash', label: 'Cash In/Out', icon: Wallet },
]

const productionItems: { key: NavKey; label: string; icon: typeof LayoutGrid }[] = [
  { key: 'production', label: 'Production', icon: Factory },
]

function GroupLabel({ children }: { children: string }) {
  return (
    <div
      style={{
        fontSize: 11,
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
        color: 'var(--color-accent-700)',
        padding: 'var(--space-2) var(--space-3) var(--space-1)',
      }}
    >
      {children}
    </div>
  )
}

function NavButton({
  label,
  icon: Icon,
  active,
  onClick,
}: {
  label: string
  icon: typeof LayoutGrid
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      className="btn"
      onClick={onClick}
      style={{
        justifyContent: 'flex-start',
        gap: 10,
        width: '100%',
        border: 'none',
        padding: '9px var(--space-3)',
        background: active ? 'var(--color-accent-100)' : 'transparent',
        color: active ? 'var(--color-accent-800)' : 'var(--color-text)',
      }}
    >
      <Icon size={18} strokeWidth={1.5} />
      <span style={{ fontSize: 14 }}>{label}</span>
    </button>
  )
}

export function Sidebar({
  active,
  onSelect,
}: {
  active: NavKey
  onSelect: (key: NavKey) => void
}) {
  return (
    <Blueprint
      as="nav"
      style={{
        width: 240,
        flex: 'none',
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-1)',
        padding: 'var(--space-3)',
        height: '100%',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-heading)',
          fontWeight: 'var(--font-heading-weight)',
          fontSize: 18,
          padding: 'var(--space-2) var(--space-3) var(--space-3)',
          borderBottom: '1px solid var(--color-divider)',
          marginBottom: 'var(--space-2)',
        }}
      >
        SMEDesk
      </div>

      <GroupLabel>Management</GroupLabel>
      {managementItems.map((item) => (
        <NavButton
          key={item.key}
          label={item.label}
          icon={item.icon}
          active={active === item.key}
          onClick={() => onSelect(item.key)}
        />
      ))}

      <GroupLabel>Accounting</GroupLabel>
      {accountingItems.map((item) => (
        <NavButton
          key={item.key}
          label={item.label}
          icon={item.icon}
          active={active === item.key}
          onClick={() => onSelect(item.key)}
        />
      ))}

      <GroupLabel>Production</GroupLabel>
      {productionItems.map((item) => (
        <NavButton
          key={item.key}
          label={item.label}
          icon={item.icon}
          active={active === item.key}
          onClick={() => onSelect(item.key)}
        />
      ))}

      <div style={{ flex: 1 }} />

      <NavButton
        label="Settings"
        icon={Settings}
        active={active === 'settings'}
        onClick={() => onSelect('settings')}
      />
    </Blueprint>
  )
}
