export default defineNuxtRouteMiddleware((to, from) => {
  const { token, role } = useAuth()

  if (token.value && role.value) {
    return navigateTo(role.value === 'parent' ? '/parent' : '/child')
  }
})
