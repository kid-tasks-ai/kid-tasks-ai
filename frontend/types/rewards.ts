export interface Reward {
    id: number
    child_id: number
    name: string
    description: string
    points_cost: number
    is_active: boolean
    is_redeemed: boolean
    category?: string
    created_at: string
    updated_at?: string
}

export interface RewardFormData {
    child_id: number
    name: string
    description: string
    points_cost: number
    is_active?: boolean
    category?: string
}

export interface RewardFilters {
    childId: number
    isActive?: boolean
    isRedeemed?: boolean
}