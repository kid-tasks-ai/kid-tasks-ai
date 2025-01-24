// plugins/auth.js
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(async (nuxtApp) => {
    const auth = useAuthStore()
    const config = useRuntimeConfig()

    // Перехватчик для всех fetch запросов
    nuxtApp.hooks.hook('app:created', () => {
        const originalFetch = globalThis.$fetch

        const isExpectedError = (error) => {
            return error.expected === true ||
                error.response?.status === 400 ||
                error.status === 400
        }

        const retryRequestWithNewToken = async (url, options = {}) => {
            const newToken = auth.token.value
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${newToken}`
            }
            try {
                return await originalFetch(url, options)
            } catch (retryError) {
                // Проверяем на ожидаемые ошибки и после refresh token
                if (isExpectedError(retryError)) {
                    const errorDetail = retryError.response?._data?.detail || retryError.message
                    throw {
                        expected: true,
                        status: retryError.response?.status,
                        message: errorDetail,
                        data: {
                            detail: errorDetail
                        }
                    }
                }
                throw retryError
            }
        }

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
                if (error.status === 401) {
                    try {
                        await auth.refreshAuthToken()
                        // Повторяем оригинальный запрос с новым токеном
                        return await retryRequestWithNewToken(url, options)
                    } catch (refreshError) {
                        // Проверяем, не является ли ошибка ожидаемой
                        if (isExpectedError(refreshError)) {
                            throw {
                                expected: true,
                                status: refreshError.response?.status,
                                message: refreshError.response?._data?.detail || refreshError.message,
                                data: {
                                    detail: refreshError.response?._data?.detail || refreshError.message
                                }
                            }
                        }
                        // Только для неожиданных ошибок делаем разлогин
                        auth.clearAuth()
                        navigateTo('/auth')
                        throw refreshError
                    }
                }

                // Для ожидаемых ошибок (400 и т.д.)
                if (isExpectedError(error)) {
                    const errorDetail = error.response?._data?.detail || error.message
                    throw {
                        expected: true,
                        status: error.response?.status,
                        message: errorDetail,
                        data: {
                            detail: errorDetail
                        }
                    }
                }

                // Для остальных ошибок
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
            if (error.status === 401) {
                try {
                    await auth.refreshAuthToken()
                } catch (refreshError) {
                    auth.clearAuth()
                    navigateTo('/auth')
                }
            }
        }
    }
})