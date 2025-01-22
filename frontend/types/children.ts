export interface Child {
    id: number
    parent_id: number
    email: string
    name: string
    age: number
    interests?: string
    preferences?: string
    points_balance: number
    role: 'child'
}

export interface ChildFormData {
    email: string
    name: string
    age: number
    interests?: string
    preferences?: string
    password?: string
}