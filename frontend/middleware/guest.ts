import { useAuthStore } from '~/stores/auth'
export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuthStore()

  if (auth.isAuthenticated.value) {
    return navigateTo(auth.isParent.value ? '/parent' : '/child')
  }
})
