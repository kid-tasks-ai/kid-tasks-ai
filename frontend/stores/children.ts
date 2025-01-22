import { Child, ChildFormData } from '~/types/children'
import { useAuthStore } from './auth'

export const useChildrenStore = () => {
    // State
    const children = useState<Child[]>('children', () => [])
    const loading = useState<boolean>('children_loading', () => false)
    const error = useState<string | null>('children_error', () => null)

    // Helpers
    function getHeaders(): Record<string, string> {
        const auth = useAuthStore()
        if (!auth.token.value) {
            throw new Error('No auth token found')
        }
        return {
            'Authorization': `Bearer ${auth.token.value}`,
            'Content-Type': 'application/json'
        }
    }

    // Actions
    async function fetchChildren(): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            children.value = await $fetch<Child[]>('/api/v1/children', {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error fetching children:', err)
            error.value = 'Не удалось загрузить список детей'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function createChild(data: ChildFormData): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch<Child>('/api/v1/children', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data,
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            const errorMessage = (err as { data?: { detail: string } })?.data?.detail
            error.value = errorMessage || 'Ошибка при создании профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateChild(id: number, data: Partial<ChildFormData>): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch<Child>(`/api/v1/children/${id}`, {
                baseURL: config.public.apiBase,
                method: 'PUT',
                body: data,
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            const errorMessage = (err as { data?: { detail: string } })?.data?.detail
            error.value = errorMessage || 'Ошибка при обновлении профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function deleteChild(id: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch(`/api/v1/children/${id}`, {
                baseURL: config.public.apiBase,
                method: 'DELETE',
                headers: getHeaders()
            })
            await fetchChildren()
        } catch (err) {
            const errorMessage = (err as { data?: { detail: string } })?.data?.detail
            error.value = errorMessage || 'Ошибка при удалении профиля'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        // State
        children,
        loading,
        error,
        // Actions
        fetchChildren,
        createChild,
        updateChild,
        deleteChild
    }
}

export type ChildrenStore = ReturnType<typeof useChildrenStore>
