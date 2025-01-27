<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between items-center">
          <!-- Логотип -->
          <div class="flex flex-shrink-0 items-center">
            <span class="text-xl font-bold">{{ title }}</span>
          </div>

          <!-- Десктопное меню -->
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

          <!-- Баллы и кнопка меню на мобильных -->
          <div class="flex items-center gap-4">
            <div v-if="profileStore.loading.value" class="flex items-center gap-2">
              <UIcon name="i-heroicons-star" class="text-yellow-500 animate-pulse" />
              <span class="font-medium">Загрузка...</span>
            </div>
            <div v-else class="flex items-center gap-2">
              <UIcon name="i-heroicons-star" class="text-yellow-500" />
              <span class="font-medium">{{ profileStore.pointsBalance }} баллов</span>
            </div>

            <!-- Мобильное меню -->
            <div class="sm:hidden">
              <UButton
                  icon="i-heroicons-bars-3"
                  color="gray"
                  variant="ghost"
                  @click="isMenuOpen = !isMenuOpen"
              />
            </div>

            <UButton @click="logout" variant="ghost">Выйти</UButton>
          </div>
        </div>

        <!-- Мобильное выпадающее меню -->
        <div v-if="isMenuOpen" class="sm:hidden">
          <div class="space-y-1 pb-3 pt-2">
            <NuxtLink
                v-for="item in menuItems"
                :key="item.path"
                :to="item.path"
                class="block px-3 py-2 rounded-md text-base font-medium"
                :class="[isActivePath(item.path) ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600']"
                @click="isMenuOpen = false"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
      <NuxtPage />
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '~/stores/auth'
import { useChildProfileStore } from '~/stores/childProfile'

export default {
  name: 'ChildLayout',

  setup() {
    const profileStore = useChildProfileStore()
    return {
      profileStore
    }
  },

  data() {
    return {
      isMenuOpen: false,
      title: 'KidTasks',
      menuItems: [
        { path: '/child', label: 'Мои задания' },
        { path: '/child/rewards', label: 'Награды' }
      ]
    }
  },

  async created() {
    try {
      await this.profileStore.fetchProfile()
    } catch (err) {
      console.error('Ошибка загрузки профиля:', err)
      // Можно добавить уведомление об ошибке
      const { $notify } = useNuxtApp()
      $notify?.error('Не удалось загрузить данные профиля')
    }
  },

  methods: {
    logout() {
      const auth = useAuthStore()
      auth.clearAuth()
      this.$router.push('/auth')
    },

    isActivePath(path) {
      if (path === '/child') {
        return this.$route.path === path
      }
      return this.$route.path.startsWith(path)
    }
  }
}
</script>