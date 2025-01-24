// stores/childTasks.ts
import { useAuthStore } from './auth'

export interface TaskAssignment {
    id: number
    template_id: number
    points_value: number
    is_completed: boolean
    is_approved: boolean
    assigned_at: string
    completed_at: string | null
    approved_at: string | null
    template: {
        title: string
        description: string
    }
}

interface TaskFilters {
    is_completed?: boolean
    is_approved?: boolean
}

export const useChildTasksStore = () => {
    // State
    const tasks = useState<TaskAssignment[]>('child_tasks', () => [])
    const loading = useState<boolean>('child_tasks_loading', () => false)
    const error = useState<string | null>('child_tasks_error', () => null)

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

    // Загрузка заданий
    async function fetchTasks(filters: TaskFilters = {}): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()
            const auth = useAuthStore()

            // Формируем параметры запроса
            const params = new URLSearchParams()
            if (filters.is_completed !== undefined) {
                params.append('is_completed', String(filters.is_completed))
            }
            if (filters.is_approved !== undefined) {
                params.append('is_approved', String(filters.is_approved))
            }

            // Добавляем child_id из текущего пользователя
            tasks.value = await $fetch<TaskAssignment[]>(
                `/api/v1/me/tasks?${params.toString()}`, {
                    baseURL: config.public.apiBase,
                    headers: getHeaders()
                }
            )
        } catch (err) {
            console.error('Error fetching tasks:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось загрузить задания'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Отметка о выполнении задания
    async function completeTask(taskId: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const updatedTask = await $fetch<TaskAssignment>(
                `/api/v1/me/tasks/${taskId}/complete`,
                {
                    baseURL: config.public.apiBase,
                    method: 'POST',
                    headers: getHeaders()
                }
            )

            // Обновляем задание в списке
            tasks.value = tasks.value.map(task =>
                task.id === taskId ? updatedTask : task
            )
        } catch (err) {
            console.error('Error completing task:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось отметить задание как выполненное'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        // State
        tasks,
        loading,
        error,
        // Actions
        fetchTasks,
        completeTask
    }
}

export type ChildTasksStore = ReturnType<typeof useChildTasksStore>