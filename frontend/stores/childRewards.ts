// stores/childRewards.ts
import { useAuthStore } from './auth'

export interface Reward {
    id: number
    name: string
    description: string | null
    points_cost: number
    is_active: boolean
    is_redeemed: boolean
    created_at: string
    redeemed_at: string | null
}

export interface RewardFilters {
    is_redeemed?: boolean
    is_active?: boolean
}

export const useChildRewardsStore = () => {
    // State
    const rewards = useState<Reward[]>('child_rewards', () => [])
    const loading = useState<boolean>('child_rewards_loading', () => false)
    const error = useState<string | null>('child_rewards_error', () => null)

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

    // Загрузка наград
    async function fetchRewards(filters: RewardFilters = {}): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            // Формируем параметры запроса
            const params = new URLSearchParams()
            if (filters.is_redeemed !== undefined) {
                params.append('is_redeemed', String(filters.is_redeemed))
            }
            if (filters.is_active !== undefined) {
                params.append('is_active', String(filters.is_active))
            }

            rewards.value = await $fetch<Reward[]>(
                `/api/v1/me/rewards?${params}`,
                {
                    baseURL: config.public.apiBase,
                    headers: getHeaders()
                }
            )
        } catch (err) {
            console.error('Error fetching rewards:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось загрузить награды'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Получение награды
    async function redeemReward(rewardId: number): Promise<Reward> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            const redeemedReward = await $fetch<Reward>(
                `/api/v1/me/rewards/${rewardId}/redeem`,
                {
                    baseURL: config.public.apiBase,
                    method: 'POST',
                    headers: getHeaders()
                }
            )

            // Обновляем награду в списке
            rewards.value = rewards.value.map(reward =>
                reward.id === rewardId ? redeemedReward : reward
            )

            return redeemedReward
        } catch (err) {
            console.error('Error redeeming reward:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось получить награду'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Получение награды по ID
    function getRewardById(id: number): Reward | undefined {
        return rewards.value.find(reward => reward.id === id)
    }

    return {
        // State
        rewards,
        loading,
        error,
        // Actions
        fetchRewards,
        redeemReward,
        getRewardById
    }
}

export type ChildRewardsStore = ReturnType<typeof useChildRewardsStore>