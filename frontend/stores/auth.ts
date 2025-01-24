// stores/auth.ts
import { AuthTokens, LoginCredentials, RegisterData, UserRole, AuthError } from '~/types/auth';

export const useAuthStore = () => {
    // State
    const token = useState<string | null>('auth_token', () => {
        if (process.client) {
            return localStorage.getItem('auth_token');
        }
        return null;
    });

    const refreshToken = useState<string | null>('refresh_token', () => {
        if (process.client) {
            return localStorage.getItem('refresh_token');
        }
        return null;
    });

    const role = useState<UserRole | null>('auth_role', () => {
        if (process.client) {
            return localStorage.getItem('auth_role') as UserRole;
        }
        return null;
    });

    // Действия с localStorage
    const setLocalStorage = (tokens: AuthTokens): void => {
        if (process.client) {
            localStorage.setItem('auth_token', tokens.access_token);
            localStorage.setItem('refresh_token', tokens.refresh_token);
            localStorage.setItem('auth_role', tokens.role);
        }
    };

    const clearLocalStorage = (): void => {
        if (process.client) {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('auth_role');
        }
    };

    // Actions
    const setAuth = (tokens: AuthTokens): void => {
        token.value = tokens.access_token;
        refreshToken.value = tokens.refresh_token;
        role.value = tokens.role;
        setLocalStorage(tokens);
    };

    const clearAuth = (): void => {
        token.value = null;
        refreshToken.value = null;
        role.value = null;
        clearLocalStorage();
    };

    const login = async (email: string, password: string): Promise<UserRole> => {
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const config = useRuntimeConfig();
            const response = await $fetch<AuthTokens>('/api/v1/auth/login', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: formData
            });

            setAuth(response);
            return response.role;
        } catch (error) {
            console.error('Login error:', error);
            throw error as AuthError;
        }
    };

    const register = async (data: RegisterData): Promise<UserRole> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<AuthTokens>('/api/v1/auth/register', {
                baseURL: config.public.apiBase,
                method: 'POST',
                body: data
            });

            setAuth(response);
            return response.role;
        } catch (error) {
            console.error('Register error:', error);
            throw error as AuthError;
        }
    };

    const refreshAuthToken = async (): Promise<void> => {
        if (!refreshToken.value) {
            throw new Error('No refresh token available');
        }

        try {
            const config = useRuntimeConfig();
            const response = await $fetch<AuthTokens>(`/api/v1/auth/refresh?refresh_token=${refreshToken.value}`, {
                baseURL: config.public.apiBase,
                method: 'POST'
            });

            setAuth(response);
        } catch (error) {
            console.error('Token refresh error:', error);
            clearAuth();
            throw error as AuthError;
        }
    };

    // Computed
    const isAuthenticated = computed(() => !!token.value);
    const isParent = computed(() => role.value === 'parent');
    const isChild = computed(() => role.value === 'child');

    return {
        // State
        token,
        refreshToken,
        role,
        // Computed
        isAuthenticated,
        isParent,
        isChild,
        // Actions
        login,
        register,
        refreshAuthToken,
        setAuth,
        clearAuth
    };
};

export type AuthStore = ReturnType<typeof useAuthStore>;