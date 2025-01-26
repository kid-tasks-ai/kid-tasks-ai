// middleware/child.ts
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to, from) => {
    const auth = useAuthStore()

    if (!auth.isChild.value) {
        return navigateTo('/auth')
    }
})