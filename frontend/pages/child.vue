<!-- layouts/child.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between">
          <div class="flex">
            <div class="flex flex-shrink-0 items-center">
              <span class="text-xl font-bold">KidTasks</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink
                  v-for="item in menuItems"
                  :key="item.path"
                  :to="item.path"
                  class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                  :class="[
                    isActivePath(item.path)
                      ? 'border-b-2 border-indigo-500 text-gray-900'
                      : 'text-gray-500'
                  ]"
              >
                {{ item.label }}
              </NuxtLink>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <span class="text-sm text-gray-600">
              <span class="font-medium">{{ childName }}</span>
            </span>

            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-star" class="text-yellow-500" />
              <span class="font-medium">{{ pointsBalance }} баллов</span>
            </div>

            <UButton @click="logout" variant="ghost">Выйти</UButton>
          </div>
        </div>
      </div>
    </nav>

    <div v-if="loading" class="fixed inset-0 bg-white bg-opacity-75 flex items-center justify-center">
      <UProgress />
    </div>

    <UAlert
        v-if="error"
        :title="error"
        color="red"
        variant="solid"
        class="m-4"
    />

    <main v-if="!loading && !error" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
      <NuxtPage />
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '~/stores/auth'
import { useChildProfileStore } from '~/stores/childProfile'

definePageMeta({
  middleware: ['child']
})

export default defineComponent({
  name: 'ChildLayout',

  layout: 'child',

  data() {
    return {
      menuItems: [
        { path: '/child', label: 'Мои задания' },
        { path: '/child/rewards', label: 'Награды' }
      ]
    }
  },

  computed: {
    profileStore() {
      return useChildProfileStore()
    },
    childName() {
      return this.profileStore.childName.value
    },
    pointsBalance() {
      return this.profileStore.pointsBalance.value
    },
    loading() {
      return this.profileStore.loading.value
    },
    error() {
      return this.profileStore.error.value
    }
  },

  async mounted() {
    try {
      await this.profileStore.fetchProfile()
    } catch (err) {
      console.error('Failed to load profile:', err)
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
})
</script>