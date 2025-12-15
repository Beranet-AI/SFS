import { CurrentUser } from '@/types/User.dto'
import { userVM } from '@/view-models/user/userVM'
import {
  userRoleLabel,
  userRoleCapabilities,
} from '@/policies/user/userRolePolicy'

export function mapUserToVM(user: CurrentUser): userVM {
  const caps = userRoleCapabilities(user.role)

  return {
    id: user.id,
    role: user.role,
    roleLabel: userRoleLabel(user.role),

    ...caps,
  }
}
