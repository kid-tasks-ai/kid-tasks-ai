<template>
  <nav class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <span class="text-xl font-bold">{{ title }}</span>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <NuxtLink
                v-for="item in menuItems"
                :key="item.path"
                :to="item.path"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="[isActivePath(item.path) ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500']"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
        </div>
        <div class="flex items-center">
          <UButton @click="logout" variant="ghost">Выйти</UButton>
        </div>
      </div>
    </div>
  </nav>

  <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <NuxtPage />
  </main>
</template>

<script>
import { useAuthStore } from '~/stores/auth'

export default {
  name: 'ParentLayout',

  data() {
    return {
      title: 'KidTasks',
      menuItems: [
        { path: '/parent', label: 'Профиль' },
        { path: '/parent/children', label: 'Дети' },
        { path: '/parent/templates', label: 'Шаблоны заданий' },
        { path: '/parent/tasks', label: 'Управление заданиями' },
        { path: '/parent/rewards', label: 'Награды' },
        { path: '/parent/statistics', label: 'Статистика' }
      ]
    }
  },

  methods: {
    logout() {
      const auth = useAuthStore()
      auth.clearAuth()
      this.$router.push('/auth')
    },

    isActivePath(path) {
      if (path === '/parent') {
        return this.$route.path === path
      }
      return this.$route.path.startsWith(path)
    }
  }
}
</script>