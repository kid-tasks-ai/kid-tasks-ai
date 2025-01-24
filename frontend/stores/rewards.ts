// stores/rewards.ts
import { Reward, RewardFormData, RewardFilters } from '~/types/rewards'
import { useAuthStore } from './auth'

export const useRewardsStore = () => {
    // State
    const rewards = useState<Reward[]>('rewards', () => [])
    const loading = useState<boolean>('rewards_loading', () => false)
    const error = useState<string | null>('rewards_error', () => null)

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

    // Загрузка наград с учетом фильтров
    async function fetchRewards(filters: RewardFilters): Promise<void> {
        try {
            if (!filters.childId) {
                rewards.value = []
                return
            }

            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            // Формируем параметры запроса
            const params = new URLSearchParams({
                child_id: filters.childId.toString()
            })

            if (filters.isActive === 'true' || filters.isActive === 'false') {
                params.append('is_active', String(filters.isActive))
            }

            if (filters.isRedeemed === 'true' || filters.isRedeemed === 'false') {
                params.append('is_redeemed', String(filters.isRedeemed))
            }

            rewards.value = await $fetch<Reward[]>(`/api/v1/rewards?${params}`, {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error fetching rewards:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось загрузить список наград'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Создание новой награды
    async function createReward(data: RewardFormData): Promise<Reward> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const newReward = await $fetch<Reward>('/api/v1/rewards', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data,
                headers: getHeaders()
            })

            // Обновляем список наград
            rewards.value = [...rewards.value, newReward]
            return newReward
        } catch (err) {
            console.error('Error creating reward:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось создать награду'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Обновление награды
    async function updateReward(id: number, data: Partial<RewardFormData>): Promise<Reward> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const updatedReward = await $fetch<Reward>(`/api/v1/rewards/${id}`, {
                baseURL: config.public.apiBase,
                method: 'PUT',
                body: data,
                headers: getHeaders()
            })

            // Обновляем награду в списке
            rewards.value = rewards.value.map(r =>
                r.id === id ? updatedReward : r
            )

            return updatedReward
        } catch (err) {
            console.error('Error updating reward:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось обновить награду'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Удаление награды
    async function deleteReward(id: number): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            await $fetch(`/api/v1/rewards/${id}`, {
                baseURL: config.public.apiBase,
                method: 'DELETE',
                headers: getHeaders()
            })

            // Удаляем награду из списка
            rewards.value = rewards.value.filter(r => r.id !== id)
        } catch (err) {
            console.error('Error deleting reward:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось удалить награду'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        // State
        rewards,
        loading,
        error,
        // Actions
        fetchRewards,
        createReward,
        updateReward,
        deleteReward
    }
}

export type RewardsStore = ReturnType<typeof useRewardsStore>