import type { ReactNode } from 'react'

const corners = ['tl', 'tr', 'bl', 'br'] as const

export function Corners() {
  return (
    <>
      {corners.map((c) => (
        <i key={c} className={`corner ${c}`} />
      ))}
    </>
  )
}

export function Blueprint({
  as: Tag = 'div',
  className = '',
  children,
  ...rest
}: {
  as?: 'div' | 'section' | 'nav'
  className?: string
  children: ReactNode
  [key: string]: unknown
}) {
  return (
    <Tag className={`blueprint ${className}`} {...rest}>
      <Corners />
      {children}
    </Tag>
  )
}
