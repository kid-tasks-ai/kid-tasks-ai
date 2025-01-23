interface Template {
    id: number;
    child_id: number;
    title: string;
    description: string;
    points_value: number;
    category?: string;
    is_active: boolean;
    schedule_type: 'once' | 'daily' | 'weekly';
    schedule_settings?: Record<string, any>;
    created_at: string;
    updated_at?: string;
}

interface TemplateFormData {
    title: string;
    description: string;
    points_value: number;
    category?: string;
    schedule_type: string;
    schedule_settings?: Record<string, any>;
    child_id: number;
}

interface TemplateFilters {
    childId?: number;
    category?: string;
    status?: boolean;
}