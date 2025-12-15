import { useMemo } from 'react'
import type { CurrentUser } from '@/types/User.dto'
import { mapUserToVM } from '@/mappers/user/userMapper'

export function useCurrentUser(user?: CurrentUser) {
  return useMemo(() => (user ? mapUserToVM(user) : null), [user])
}
