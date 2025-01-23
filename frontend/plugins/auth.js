// plugins/auth.js
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(async (nuxtApp) => {
    const auth = useAuthStore()
    const config = useRuntimeConfig()

    // Перехватчик для всех fetch запросов
    nuxtApp.hooks.hook('app:created', () => {
        const originalFetch = globalThis.$fetch
        globalThis.$fetch = async (url, options = {}) => {
            try {
                // Добавляем токен к запросу если есть
                if (auth.token.value) {
                    options.headers = {
                        ...options.headers,
                        'Authorization': `Bearer ${auth.token.value}`
                    }
                }

                return await originalFetch(url, options)
            } catch (error) {
                // Если получили 401, пробуем обновить токен
                if (error.status === 401 && auth.refreshToken.value) {
                    try {
                        await auth.refreshAuth()
                        // Повторяем оригинальный запрос с новым токеном
                        options.headers = {
                            ...options.headers,
                            'Authorization': `Bearer ${auth.token.value}`
                        }
                        return await originalFetch(url, options)
                    } catch (refreshError) {
                        // Если не удалось обновить токен - разлогиниваем
                        auth.clearAuth()
                        navigateTo('/auth')
                        throw refreshError
                    }
                }
                throw error
            }
        }
    })

    // Проверяем валидность токена при старте
    if (auth.token.value) {
        try {
            await $fetch('/api/v1/auth/verify', {
                baseURL: config.public.apiBase,
                headers: { 'Authorization': `Bearer ${auth.token.value}` }
            })
        } catch (error) {
            if (error.status === 401 && auth.refreshToken.value) {
                try {
                    await auth.refreshAuth()
                } catch (refreshError) {
                    auth.clearAuth()
                    navigateTo('/auth')
                }
            }
        }
    }
})