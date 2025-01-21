export default defineNuxtRouteMiddleware((to, from) => {
  const { token, role } = useAuth()

  if (!token.value || role.value !== 'parent') {
    return navigateTo('/auth')
  }
})