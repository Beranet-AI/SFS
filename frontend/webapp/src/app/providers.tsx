'use client'

import { LiveStatusProvider } from '@/ui/live-status/components/liveStatusProvider'

export function Providers({ children }: { children: React.ReactNode }) {
  return <LiveStatusProvider>{children}</LiveStatusProvider>
}
