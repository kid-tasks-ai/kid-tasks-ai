export const useAuthStore = () => {
    const token = useState('auth_token', () => localStorage.getItem('auth_token'))
    const role = useState('auth_role', () => localStorage.getItem('auth_role'))

    return {
        // State
        token,
        role,
        // Getters
        isAuthenticated: computed(() => !!token.value),
        isParent: computed(() => role.value === 'parent'),
        isChild: computed(() => role.value === 'child'),
        // Actions
        setAuth: (newToken, newRole) => {
            token.value = newToken
            role.value = newRole
            localStorage.setItem('auth_token', newToken)
            localStorage.setItem('auth_role', newRole)
        },
        clearAuth: () => {
            token.value = null
            role.value = null
            localStorage.removeItem('auth_token')
            localStorage.removeItem('auth_role')
        }
    }
}