import { useEffect, useState } from 'react'
import { get, paths } from '../../lib/api'

export function Header() {
  const [healthy, setHealthy] = useState<boolean | null>(null)
  const base = import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080'

  useEffect(() => {
    get(paths.health).then(() => setHealthy(true)).catch(() => setHealthy(false))
  }, [])

  return (
    <header className="header border-b border-[#2a2b32]">
      <div className="px-4 sm:px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="/favicon.svg"
              width={28}
              height={28}
              alt="logo"
              className="rounded-lg"
            />
            <div className="text-base sm:text-lg font-semibold">
              Multi-Modal Agentic AI Agent
            </div>
          </div>
          <div className="flex items-center text-xs sm:text-sm font-mono text-[#c5c5d1]">
            <span
              className={`inline-block h-2.5 w-2.5 rounded-full ${
                healthy === false ? 'bg-rose-500' : 'bg-emerald-500'
              }`}
            />
            <span className="ml-2">{base}</span>
          </div>
        </div>
      </div>
    </header>
  )
}
