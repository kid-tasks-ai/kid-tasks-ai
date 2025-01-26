// stores/templates.ts
import { Template, TemplateFormData, TemplateFilters } from '~/types/templates'
import { useAuthStore } from './auth'

export const useTemplatesStore = () => {
    // State
    const templates = useState<Template[]>('templates', () => [])
    const loading = useState<boolean>('templates_loading', () => false)
    const error = useState<string | null>('templates_error', () => null)

    // Получение заголовков с токеном авторизации
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

    // Загрузка шаблонов с учетом фильтров
    async function fetchTemplates(filters: TemplateFilters): Promise<void> {
        try {
            if (!filters.childId) {
                templates.value = []
                return
            }

            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            // Формируем параметры запроса
            const params = new URLSearchParams({
                child_id: filters.childId.toString()
            })

            if (filters.status === 'true' || filters.status === 'false') {
                params.append('is_active', filters.status)
            }

            templates.value = await $fetch<Template[]>(`/api/v1/tasks/templates?${params}`, {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error fetching templates:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось загрузить шаблоны заданий'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Создание нового шаблона
    async function createTemplate(data: TemplateFormData): Promise<Template> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const newTemplate = await $fetch<Template>('/api/v1/tasks/templates', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data,
                headers: getHeaders()
            })

            // Обновляем список шаблонов
            templates.value = [...templates.value, newTemplate]
            return newTemplate
        } catch (err) {
            console.error('Error creating template:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось создать шаблон'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Обновление шаблона
    async function updateTemplate(id: number, data: Partial<TemplateFormData>): Promise<Template> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const updatedTemplate = await $fetch<Template>(`/api/v1/tasks/templates/${id}`, {
                baseURL: config.public.apiBase,
                method: 'PUT',
                body: data,
                headers: getHeaders()
            })

            // Обновляем шаблон в списке
            templates.value = templates.value.map(t =>
                t.id === id ? updatedTemplate : t
            )

            return updatedTemplate
        } catch (err) {
            console.error('Error updating template:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось обновить шаблон'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Удаление шаблона
    async function deleteTemplate(id: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch(`/api/v1/tasks/templates/${id}`, {
                baseURL: config.public.apiBase,
                method: 'DELETE',
                headers: getHeaders()
            })

            // Удаляем шаблон из списка
            templates.value = templates.value.filter(t => t.id !== id)
        } catch (err) {
            console.error('Error deleting template:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось удалить шаблон'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function generateTasks(data: {
        child_id: number;
        task_count: number;
        description: string;
    }): Promise<{ status: string }> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            return await $fetch<{ status: string }>('/api/v1/tasks/templates/generate', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data,
                headers: getHeaders()
            })

        } catch (err) {
            console.error('Error generating tasks:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось сгенерировать задания'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        // State
        templates,
        loading,
        error,
        // Actions
        fetchTemplates,
        createTemplate,
        updateTemplate,
        deleteTemplate,
        generateTasks
    }
}

export type TemplatesStore = ReturnType<typeof useTemplatesStore>