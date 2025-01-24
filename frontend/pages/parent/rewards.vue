<!-- pages/parent/rewards.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление наградами</h1>

    <!-- Фильтры и выбор ребенка -->
    <UCard class="mb-6">
      <div class="flex gap-4 items-end">
        <UFormGroup label="Ребёнок" class="flex-1">
          <USelect
              v-model="selectedChildId"
              :options="children"
              option-attribute="name"
              value-attribute="id"
              placeholder="Выберите ребенка"
              @change="loadRewards"
          />
        </UFormGroup>
        <UFormGroup label="Статус" class="flex-1">
          <USelect
              v-model="filters.isActive"
              :options="[
                { label: 'Все', value: null },
                { label: 'Активные', value: true },
                { label: 'Неактивные', value: false }
              ]"
              option-attribute="label"
              value-attribute="value"
              @change="loadRewards"
          />
        </UFormGroup>
        <UButton
            color="primary"
            @click="openAddRewardModal"
            :disabled="!selectedChildId"
        >
          Добавить награду
        </UButton>
      </div>
    </UCard>

    <!-- Список наград -->
    <UCard>
      <div v-if="loading" class="flex justify-center py-8">
        <UProgress />
      </div>

      <div v-else-if="error" class="text-center py-8 text-red-500">
        {{ error }}
      </div>

      <div v-else-if="!selectedChildId" class="text-center py-8 text-gray-500">
        Выберите ребенка для отображения наград
      </div>

      <div v-else-if="rewards.length === 0" class="text-center py-8 text-gray-500">
        Нет доступных наград. Добавьте первую награду для ребенка!
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard
            v-for="reward in rewards"
            :key="reward.id"
            class="bg-gray-50"
        >
          <template #header>
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium">{{ reward.name }}</h3>
              <UBadge
                  :color="reward.is_active ? 'green' : 'gray'"
                  variant="subtle"
              >
                {{ reward.is_active ? 'Активна' : 'Неактивна' }}
              </UBadge>
            </div>
          </template>

          <div class="space-y-2">
            <p class="text-gray-600">{{ reward.description }}</p>
            <div class="flex justify-between items-center">
              <span class="font-medium">Стоимость: {{ reward.points_cost }} баллов</span>
              <UBadge
                  v-if="reward.is_redeemed"
                  color="purple"
                  variant="subtle"
              >
                Погашена
              </UBadge>
            </div>
          </div>

          <template #footer>
            <div class="flex justify-end space-x-2">
              <UButton
                  @click="editReward(reward)"
                  variant="ghost"
                  icon="i-heroicons-pencil"
              >
                Изменить
              </UButton>
              <UButton
                  @click="confirmDelete(reward)"
                  variant="ghost"
                  color="red"
                  icon="i-heroicons-trash"
              >
                Удалить
              </UButton>
            </div>
          </template>
        </UCard>
      </div>
    </UCard>

    <!-- Модальное окно для создания/редактирования награды -->
    <UModal v-model="showRewardModal">
      <template #default>
        <div class="p-4">
          <h2 class="text-lg font-medium mb-4">
            {{ editingReward ? 'Редактировать награду' : 'Добавить награду' }}
          </h2>

          <form @submit.prevent="saveReward" class="space-y-4">
            <UFormGroup label="Название награды" required>
              <UInput
                  v-model="rewardForm.name"
                  placeholder="Введите название награды"
                  required
              />
            </UFormGroup>

            <UFormGroup label="Описание" required>
              <UTextarea
                  v-model="rewardForm.description"
                  placeholder="Опишите награду"
                  :rows="3"
                  required
              />
            </UFormGroup>

            <UFormGroup label="Стоимость (в баллах)" required>
              <UInput
                  v-model.number="rewardForm.points_cost"
                  type="number"
                  min="1"
                  placeholder="Введите стоимость в баллах"
                  required
              />
            </UFormGroup>

            <UFormGroup>
              <UToggle v-model="rewardForm.is_active">
                <span class="ml-2">Награда активна</span>
              </UToggle>
            </UFormGroup>

            <div class="flex justify-end space-x-2">
              <UButton
                  type="button"
                  variant="ghost"
                  @click="closeRewardModal"
              >
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
        </div>
      </template>
    </UModal>
  </div>
</template>

<script>
import { useChildrenStore } from '~/stores/children'
import { useRewardsStore } from '~/stores/rewards'

export default {
  name: 'RewardsPage',
  layout: 'parent',
  middleware: ['parent'],

  data() {
    return {
      selectedChildId: null,
      filters: {
        isActive: null
      },
      showRewardModal: false,
      editingReward: null,
      saving: false,
      rewardForm: {
        name: '',
        description: '',
        points_cost: 1,
        is_active: true
      },
      children: [],
      rewards: [],
      loading: false,
      error: null
    }
  },

  async created() {
    await this.loadChildren()
  },

  methods: {
    async loadChildren() {
      try {
        const childrenStore = useChildrenStore()
        await childrenStore.fetchChildren()
        this.children = childrenStore.children.value

        if (this.children.length > 0) {
          this.selectedChildId = this.children[0].id
          await this.loadRewards()
        }
      } catch (err) {
        console.error('Ошибка загрузки детей:', err)
        this.error = 'Не удалось загрузить список детей'
      }
    },

    async loadRewards() {
      if (!this.selectedChildId) return

      try {
        this.loading = true
        this.error = null
        const rewardsStore = useRewardsStore()
        await rewardsStore.fetchRewards({
          childId: this.selectedChildId,
          isActive: this.filters.isActive
        })
        this.rewards = rewardsStore.rewards.value
      } catch (err) {
        console.error('Ошибка загрузки наград:', err)
        this.error = 'Не удалось загрузить список наград'
      } finally {
        this.loading = false
      }
    },

    openAddRewardModal() {
      if (!this.selectedChildId) return

      this.editingReward = null
      this.rewardForm = {
        name: '',
        description: '',
        points_cost: 1,
        is_active: true
      }
      this.showRewardModal = true
    },

    editReward(reward) {
      this.editingReward = reward
      this.rewardForm = {
        name: reward.name,
        description: reward.description,
        points_cost: reward.points_cost,
        is_active: reward.is_active
      }
      this.showRewardModal = true
    },

    async saveReward() {
      try {
        this.saving = true
        const rewardsStore = useRewardsStore()

        const formData = {
          ...this.rewardForm,
          child_id: this.selectedChildId
        }

        if (this.editingReward) {
          await rewardsStore.updateReward(this.editingReward.id, formData)
        } else {
          await rewardsStore.createReward(formData)
        }

        await this.loadRewards()
        this.closeRewardModal()
      } catch (err) {
        console.error('Ошибка сохранения награды:', err)
        this.error = 'Не удалось сохранить награду'
      } finally {
        this.saving = false
      }
    },

    closeRewardModal() {
      this.showRewardModal = false
      this.editingReward = null
      this.rewardForm = {
        name: '',
        description: '',
        points_cost: 1,
        is_active: true
      }
    },

    async confirmDelete(reward) {
      if (confirm(`Вы уверены, что хотите удалить награду "${reward.name}"?`)) {
        try {
          const rewardsStore = useRewardsStore()
          await rewardsStore.deleteReward(reward.id)
          await this.loadRewards()
        } catch (err) {
          console.error('Ошибка удаления награды:', err)
          this.error = 'Не удалось удалить награду'
        }
      }
    }
  }
}
</script>