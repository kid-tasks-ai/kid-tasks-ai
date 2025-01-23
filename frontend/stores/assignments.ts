// stores/assignments.ts
import { Assignment, AssignmentFilters } from '~/types/assignments'
import { useAuthStore } from './auth'

export const useAssignmentsStore = () => {
    // State
    const assignments = useState<Assignment[]>('assignments', () => [])
    const loading = useState<boolean>('assignments_loading', () => false)
    const error = useState<string | null>('assignments_error', () => null)

    // Получение заголовков с токеном
    function getHeaders(): Record<string, string> {
        const auth = useAuthStore()
        if (!auth.token.value) {
            throw new Error('Не авторизован')
        }
        return {
            'Authorization': `Bearer ${auth.token.value}`,
            'Content-Type': 'application/json'
        }
    }

    // Загрузка заданий с фильтрами
    async function fetchAssignments(filters: AssignmentFilters): Promise<void> {
        // Проверяем наличие обязательного параметра
        if (!filters.childId) {
            assignments.value = []
            error.value = 'Не указан ID ребенка'
            return
        }

        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const queryParams = new URLSearchParams()
            queryParams.append('child_id', String(filters.childId))

            if (filters.isCompleted === 'true' || filters.isCompleted === 'false') {
                queryParams.append('is_completed', String(filters.isCompleted))
            }
            if (filters.isApproved === 'true' || filters.isApproved === 'false') {
                queryParams.append('is_approved', String(filters.isApproved))
            }

            const url = `/api/v1/tasks/assignments?${queryParams.toString()}`
            assignments.value = await $fetch(url, {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error fetching assignments:', err)
            error.value = err?.data?.detail || 'Не удалось загрузить задания'
            throw err
        } finally {
            loading.value = false
        }
    }


    // Создание задания из шаблона
    async function createFromTemplate(templateId: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch(`/api/v1/tasks/templates/${templateId}/assign`, {
                baseURL: config.public.apiBase,
                method: 'POST',
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error creating assignment:', err)
            error.value = 'Не удалось создать задание'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Одобрение выполненного задания
    async function approveAssignment(assignmentId: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch(`/api/v1/tasks/assignments/${assignmentId}/approve`, {
                baseURL: config.public.apiBase,
                method: 'PUT',
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error approving assignment:', err)
            error.value = 'Не удалось одобрить задание'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        // State
        assignments,
        loading,
        error,
        // Actions
        fetchAssignments,
        createFromTemplate,
        approveAssignment
    }
}

export type AssignmentsStore = ReturnType<typeof useAssignmentsStore>