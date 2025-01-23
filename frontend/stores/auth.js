// stores/auth.js
export const useAuthStore = () => {
    const token = useState('auth_token', () => localStorage.getItem('auth_token'))
    const refreshToken = useState('refresh_token', () => localStorage.getItem('refresh_token'))
    const role = useState('auth_role', () => localStorage.getItem('auth_role'))

    const setAuth = (newToken, newRefreshToken, newRole) => {
        token.value = newToken
        refreshToken.value = newRefreshToken
        role.value = newRole
        localStorage.setItem('auth_token', newToken)
        localStorage.setItem('refresh_token', newRefreshToken)
        localStorage.setItem('auth_role', newRole)
    }

    const clearAuth = () => {
        token.value = null
        refreshToken.value = null
        role.value = null
        localStorage.removeItem('auth_token')
        localStorage.removeItem('refresh_token')
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
            setAuth(response.access_token, response.refresh_token, response.role)
            return response.role
        }
        throw new Error('Ошибка авторизации')
    }

    const refreshAuth = async () => {
        if (!refreshToken.value) {
            throw new Error('Нет refresh токена')
        }

        const config = useRuntimeConfig()
        const response = await $fetch('/api/v1/auth/refresh', {
            baseURL: config.public.apiBase,
            method: 'POST',
            body: { refresh_token: refreshToken.value }
        })

        if (response?.access_token) {
            setAuth(response.access_token, response.refresh_token, role.value)
        } else {
            throw new Error('Не удалось обновить токен')
        }
    }

    const register = async (userData) => {
        const config = useRuntimeConfig()
        const response = await $fetch('/api/v1/auth/register', {
            baseURL: config.public.apiBase,
            method: 'POST',
            body: userData
        })

        if (response?.access_token) {
            setAuth(response.access_token, response.refresh_token, response.role)
            return response.role
        }
        throw new Error('Ошибка регистрации')
    }
    return {
        token,
        refreshToken,
        role,
        isAuthenticated: computed(() => !!token.value),
        isParent: computed(() => role.value === 'parent'),
        isChild: computed(() => role.value === 'child'),
        setAuth,
        clearAuth,
        login,
        register,
        refreshAuth
    }
}