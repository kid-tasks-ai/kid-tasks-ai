// types/assignments.ts

export interface Assignment {
    id: number
    template_id: number
    child_id: number
    points_value: number
    is_completed: boolean
    is_approved: boolean
    assigned_at: string
    completed_at?: string
    approved_at?: string
    template: {
        id: number
        title: string
        description: string
        schedule_type: 'once' | 'daily' | 'weekly'
    }
}

export interface AssignmentFilters {
    childId: number
    isCompleted?: boolean
    isApproved?: boolean
}