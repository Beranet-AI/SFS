'use client'

import { AlertProvider } from '@/ui/alert/components/AlertProvider'

export function Providers({ children }: { children: React.ReactNode }) {
  return <AlertProvider>{children}</AlertProvider>
}
