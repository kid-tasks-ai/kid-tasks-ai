// types/auth.ts

export type UserRole = 'parent' | 'child';

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    email: string;
    password: string;
    name: string;
}

export interface AuthTokens {
    access_token: string;
    refresh_token: string;
    token_type: string;
    role: UserRole;
}

export interface AuthState {
    token: string | null;
    refreshToken: string | null;
    role: UserRole | null;
}

export interface AuthError {
    status?: number;
    data?: {
        detail: string;
    };
}