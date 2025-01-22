// stores/auth.js
export const useAuthStore = () => {
    const token = useState('auth_token', () => localStorage.getItem('auth_token'))
    const role = useState('auth_role', () => localStorage.getItem('auth_role'))

    // Actions
    const setAuth = (newToken, newRole) => {
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

    const login = async (email, password) => {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)

        const config = useRuntimeConfig()
        const response = await $fetch('/api/v1/auth/login', {
            baseURL: config.public.apiBase,
            method: 'POST',
            body: formData
        })

        if (response?.access_token) {
            setAuth(response.access_token, response.role)
            return response.role
        }
        throw new Error('Ошибка авторизации')
    }

    const register = async (userData) => {
        const config = useRuntimeConfig()
        return await $fetch('/api/v1/auth/register', {
            baseURL: config.public.apiBase,
            method: 'POST',
            body: userData,
            headers: {
                'Content-Type': 'application/json'
            }
        })
    }

    return {
        // State
        token,
        role,
        // Getters
        isAuthenticated: computed(() => !!token.value),
        isParent: computed(() => role.value === 'parent'),
        isChild: computed(() => role.value === 'child'),
        // Actions
        setAuth,
        clearAuth,
        login,
        register
    }
}