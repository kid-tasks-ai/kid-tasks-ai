<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h1 class="text-2xl font-bold mb-4">KidTasks AI</h1>
      <p class="text-gray-600 mb-4">Загрузка...</p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['guest']
})

// Автоматическое перенаправление при загрузке страницы
onMounted(() => {
  const { token, role } = useAuth()

  if (!token.value) {
    navigateTo('/auth')
  } else {
    // Перенаправление в зависимости от роли пользователя
    navigateTo(role.value === 'parent' ? '/parent' : '/child')
  }
})
</script>