export const useAuth = () => {
  const token = useState<string | null>('auth_token', () => localStorage.getItem('auth_token'))
  const role = useState<string | null>('auth_role', () => localStorage.getItem('auth_role'))

  const setAuth = (newToken: string, newRole: string) => {
    token.value = newToken
    role.value = newRole
    localStorage.setItem('auth_token', newToken)
    localStorage.setItem('auth_role', newRole)
  }

  const clearAuth = () => {
    token.value = null
    role.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_role')
  }

  return {
    token,
    role,
    setAuth,
    clearAuth
  }
}