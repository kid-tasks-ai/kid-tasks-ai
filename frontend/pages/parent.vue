<template>
  <!-- Шапка -->
  <nav class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <span class="text-xl font-bold">KidTasks</span>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <NuxtLink
              to="/parent"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium"
              :class="[$route.path === '/parent' ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              Профиль
            </NuxtLink>
            <NuxtLink
              to="/parent/children"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium"
              :class="[$route.path.startsWith('/parent/children') ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              Дети
            </NuxtLink>
            <NuxtLink
              to="/parent/tasks"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium"
              :class="[$route.path.startsWith('/parent/tasks') ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              Задания
            </NuxtLink>
            <NuxtLink
              to="/parent/rewards"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium"
              :class="[$route.path.startsWith('/parent/rewards') ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              Награды
            </NuxtLink>
            <NuxtLink
              to="/parent/statistics"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium"
              :class="[$route.path.startsWith('/parent/statistics') ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              Статистика
            </NuxtLink>
          </div>
        </div>
        <div class="flex items-center">
          <UButton @click="logout" variant="ghost">Выйти</UButton>
        </div>
      </div>
    </div>
  </nav>

  <!-- Основной контент -->
  <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <NuxtPage />
  </main>
</template>

<script setup>
function logout() {
  const { clearAuth } = useAuth()
  clearAuth()
  navigateTo('/auth')
}

definePageMeta({
  layout: 'parent',
  middleware: ['parent']
})
</script>