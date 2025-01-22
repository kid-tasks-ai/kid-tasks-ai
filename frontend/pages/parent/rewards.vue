<!-- pages/parent/rewards.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление наградами</h1>

    <!-- Список наград -->
    <UCard class="mb-6">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-medium">Доступные награды</h2>
          <UButton @click="openAddRewardModal" color="primary">
            Добавить награду
          </UButton>
        </div>
      </template>

      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
      </div>

      <div v-else-if="error" class="text-center py-8 text-red-500">
        {{ error }}
      </div>

      <div v-else-if="rewards.length === 0" class="text-center py-8 text-gray-500">
        Нет доступных наград. Добавьте первую награду для ваших детей!
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard v-for="reward in rewards" :key="reward.id" class="bg-gray-50">
          <template #header>
            <h3 class="text-lg font-medium">{{ reward.name }}</h3>
          </template>

          <div class="space-y-2">
            <p class="text-gray-600">{{ reward.description }}</p>
            <p class="font-medium">Стоимость: {{ reward.points_cost }} баллов</p>
            <p class="text-sm" :class="reward.is_active ? 'text-green-600' : 'text-gray-500'">
              {{ reward.is_active ? 'Активна' : 'Неактивна' }}
            </p>
          </div>

          <template #footer>
            <div class="flex justify-end space-x-2">
              <UButton @click="openEditRewardModal(reward)" variant="ghost">
                Редактировать
              </UButton>
              <UButton
                  @click="toggleRewardStatus(reward)"
                  :color="reward.is_active ? 'gray' : 'primary'"
                  :variant="reward.is_active ? 'soft' : 'outline'"
                  :loading="reward.id === updatingStatusId"
              >
                {{ reward.is_active ? 'Деактивировать' : 'Активировать' }}
              </UButton>
            </div>
          </template>
        </UCard>
      </div>
    </UCard>

    <!-- Модальное окно добавления/редактирования награды -->
    <UModal
        v-model="showRewardModal"
        :title="editingReward ? 'Редактировать награду' : 'Добавить награду'"
    >
      <form @submit.prevent="saveReward" class="space-y-4">
        <UFormGroup label="Название награды" required>
          <UInput
              v-model="rewardForm.name"
              placeholder="Введите название награды"
              :error="formErrors.name"
              required
          />
        </UFormGroup>

        <UFormGroup label="Описание" required>
          <UTextarea
              v-model="rewardForm.description"
              placeholder="Опишите награду"
              :error="formErrors.description"
              rows="3"
              required
          />
        </UFormGroup>

        <UFormGroup label="Стоимость (в баллах)" required>
          <UInput
              v-model="rewardForm.points_cost"
              type="number"
              min="1"
              placeholder="Введите стоимость в баллах"
              :error="formErrors.points_cost"
              required
          />
        </UFormGroup>

        <UFormGroup>
          <div class="flex items-center">
            <UToggle v-model="rewardForm.is_active">
              <span class="ml-2">Награда активна</span>
            </UToggle>
          </div>
        </UFormGroup>

        <div class="flex justify-end space-x-2">
          <UButton @click="closeRewardModal" variant="ghost">
            Отмена
          </UButton>
          <UButton
              type="submit"
              color="primary"
              :loading="saving"
          >
            {{ editingReward ? 'Сохранить' : 'Добавить' }}
          </UButton>
        </div>
      </form>
    </UModal>
  </div>
</template>

<script>
export default {
  name: 'RewardsPage',
  layout: 'parent',
  middleware: ['parent'],
  data() {
    return {
      rewards: [],
      loading: true,
      error: null,
      showRewardModal: false,
      editingReward: null,
      saving: false,
      updatingStatusId: null,
      formErrors: {},
      rewardForm: this.getDefaultFormData()
    }
  },

  methods: {
    getDefaultFormData() {
      return {
        name: '',
        description: '',
        points_cost: 0,
        is_active: true
      }
    },

    async fetchRewards() {
      try {
        this.loading = true
        this.error = null
        const config = useRuntimeConfig()
        const response = await $fetch('/api/v1/rewards', {
          baseURL: config.public.apiBase,
          headers: useRequestHeaders(['cookie'])
        })
        this.rewards = response
      } catch (err) {
        this.error = 'Не удалось загрузить список наград'
        console.error('Error fetching rewards:', err)
      } finally {
        this.loading = false
      }
    },

    async createReward(data) {
      const config = useRuntimeConfig()
      return await $fetch('/api/v1/rewards', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: data,
        headers: useRequestHeaders(['cookie'])
      })
    },

    // ... остальные методы API и UI остаются теми же,
    // просто меняем this.rewardForm.value на this.rewardForm и т.д.
  },

  mounted() {
    this.fetchRewards()
  }
}
</script>
