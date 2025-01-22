// composables/useChildren.ts
export const useChildren = () => {
    const config = useRuntimeConfig()
    const { token } = useAuth()
    const loading = ref(false)
    const error = ref(null)
    const children = ref([])

    // Функция для получения заголовков
    const getHeaders = () => {
        if (!token.value) {
            throw new Error('No auth token found')
        }
        return {
            'Authorization': `Bearer ${token.value}`,
            'Content-Type': 'application/json'
        }
    }

    // Получение списка детей
    async function fetchChildren() {
        try {
            loading.value = true
            error.value = null
            console.log('Fetching with token:', token.value)

            children.value = await $fetch('/api/v1/children', {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Full error:', err)
            error.value = 'Не удалось загрузить список детей'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Создание профиля ребенка
    async function createChild(data) {
        try {
            loading.value = true
            error.value = null
            await $fetch('/api/v1/children', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data,
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            error.value = err.data?.detail || 'Ошибка при создании профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Обновление профиля
    async function updateChild(id, data) {
        try {
            loading.value = true
            error.value = null
            await $fetch(`/api/v1/children/${id}`, {
                baseURL: config.public.apiBase,
                method: 'PUT',
                body: data,
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            error.value = err.data?.detail || 'Ошибка при обновлении профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Удаление профиля
    async function deleteChild(id) {
        try {
            loading.value = true
            error.value = null
            await $fetch(`/api/v1/children/${id}`, {
                baseURL: config.public.apiBase,
                method: 'DELETE',
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            error.value = err.data?.detail || 'Ошибка при удалении профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        children,
        loading,
        error,
        fetchChildren,
        createChild,
        updateChild,
        deleteChild
    }
}