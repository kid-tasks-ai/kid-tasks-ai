<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h1 class="text-2xl font-bold mb-4">KidTasks AI</h1>
      <p class="text-gray-600 mb-4">Загрузка...</p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  middleware: ['guest']
})

export default {
  name: 'IndexPage',

  mounted() {
    const auth = useAuthStore()

    if (!auth.token.value) {
      this.$router.push('/auth')
    } else {
      this.$router.push(auth.role.value === 'parent' ? '/parent' : '/child')
    }
  }
}
</script>