// stores/childProfile.ts
import { useAuthStore } from './auth'

export interface ChildProfile {
    id: number;
    name: string;
    points_balance: number;
    email: string;
    age: number;
    interests: string | null;
    preferences: string | null;
}

export const useChildProfileStore = () => {
    // State
    const profile = useState<ChildProfile | null>('child_profile', () => null)
    const loading = useState<boolean>('child_profile_loading', () => false)
    const error = useState<string | null>('child_profile_error', () => null)

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

    // Загрузка профиля
    async function fetchProfile(): Promise<void> {
        try {
            loading.value = true
            error.value = null
            const config = useRuntimeConfig()

            profile.value = await $fetch<ChildProfile>('/api/v1/me', {
                baseURL: config.public.apiBase,
                headers: getHeaders()
            })
        } catch (err) {
            console.error('Error fetching profile:', err)
            const message = (err as { data?: { detail: string } })?.data?.detail
            error.value = message || 'Не удалось загрузить профиль'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Обновление баланса баллов
    function updatePointsBalance(points: number): void {
        if (profile.value) {
            profile.value = {
                ...profile.value,
                points_balance: points
            }
        }
    }

    return {
        // State
        profile,
        loading,
        error,
        // Computed
        pointsBalance: computed(() => profile.value?.points_balance ?? 0),
        childName: computed(() => profile.value?.name ?? ''),
        // Actions
        fetchProfile,
        updatePointsBalance
    }
}

export type ChildProfileStore = ReturnType<typeof useChildProfileStore>