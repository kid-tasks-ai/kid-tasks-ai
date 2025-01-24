<!-- pages/child/index.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Мои задания</h1>

    <!-- Активные задания -->
    <UCard class="mb-6">
      <template #header>
        <h2 class="text-lg font-medium">Активные задания</h2>
      </template>

      <div v-if="activeTasks.loading" class="flex justify-center py-8">
        <UProgress />
      </div>

      <UAlert
          v-else-if="activeTasks.error"
          :title="activeTasks.error"
          color="red"
          variant="soft"
          class="mb-4"
      />

      <div v-else-if="activeTasks.tasks.length === 0" class="text-center py-8">
        <UIcon name="i-heroicons-check-circle" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-semibold text-gray-900">Нет активных заданий</h3>
        <p class="mt-1 text-sm text-gray-500">Все задания выполнены!</p>
      </div>

      <div v-else class="divide-y divide-gray-200">
        <div
            v-for="task in activeTasks.tasks"
            :key="task.id"
            class="py-4"
            :class="{'bg-red-50': task.returned_at}"
        >
          <div class="flex items-start justify-between">
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <h3 class="text-base font-medium">{{ task.template.title }}</h3>
                <UBadge
                    v-if="task.returned_at"
                    color="red"
                    variant="soft"
                >
                  Требует доработки
                </UBadge>
              </div>
              <p class="text-sm text-gray-600">{{ task.template.description }}</p>
              <div v-if="task.parent_comment" class="mt-2 p-3 bg-red-100 rounded-md">
                <p class="text-sm text-red-700">
                  <span class="font-medium">Комментарий родителя:</span><br/>
                  {{ task.parent_comment }}
                </p>
                <p class="text-xs text-red-600 mt-1">
                  Возвращено: {{ formatDate(task.returned_at) }}
                </p>
              </div>
              <div class="flex items-center gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-star" class="text-yellow-500" />
                  {{ task.points_value }} баллов
                </span>
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-calendar" />
                  Назначено: {{ formatDate(task.assigned_at) }}
                </span>
              </div>
            </div>
            <UButton
                :color="task.returned_at ? 'red' : 'primary'"
                :loading="completing === task.id"
                @click="handleComplete(task)"
            >
              {{ task.returned_at ? 'Отправить заново' : 'Выполнено' }}
            </UButton>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Выполненные задания -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-medium">Выполненные задания</h2>
          <USelect
              v-model="completedFilter"
              :options="[
                { label: 'Все', value: null },
                { label: 'На проверке', value: 'pending' },
                { label: 'Одобренные', value: 'approved' }
              ]"
              option-attribute="label"
              value-attribute="value"
              class="w-40"
          />
        </div>
      </template>

      <div v-if="completedTasks.loading" class="flex justify-center py-8">
        <UProgress />
      </div>

      <UAlert
          v-else-if="completedTasks.error"
          :title="completedTasks.error"
          color="red"
          variant="soft"
          class="mb-4"
      />

      <div v-else-if="completedTasks.tasks.length === 0" class="text-center py-8">
        <UIcon name="i-heroicons-document-text" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-semibold text-gray-900">Нет выполненных заданий</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ completedFilter === 'pending' ? 'Нет заданий на проверке' : 'Начните выполнять задания!' }}
        </p>
      </div>

      <div v-else class="divide-y divide-gray-200">
        <div
            v-for="task in completedTasks.tasks"
            :key="task.id"
            class="py-4"
        >
          <div class="flex items-start justify-between">
            <div class="space-y-1">
              <h3 class="text-base font-medium">{{ task.template.title }}</h3>
              <p class="text-sm text-gray-600">{{ task.template.description }}</p>
              <div class="flex items-center gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-star" class="text-yellow-500" />
                  {{ task.points_value }} баллов
                </span>
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-calendar" />
                  Выполнено: {{ formatDate(task.completed_at) }}
                </span>
                <UBadge
                    :color="task.is_approved ? 'green' : 'yellow'"
                    :variant="task.is_approved ? 'solid' : 'soft'"
                >
                  {{ task.is_approved ? 'Одобрено' : 'На проверке' }}
                </UBadge>
              </div>
            </div>
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>

<script>
import { useChildTasksStore } from '~/stores/childTasks'

definePageMeta({
  middleware: ['child']
})

export default {
  name: 'ChildTasksPage',

  layout: 'child',

  data() {
    return {
      store: null,
      completing: null,
      completedFilter: null,
      activeTasks: {
        tasks: [],
        loading: false,
        error: null
      },
      completedTasks: {
        tasks: [],
        loading: false,
        error: null
      }
    }
  },

  watch: {
    completedFilter() {
      this.loadCompletedTasks()
    }
  },

  async created() {
    this.store = useChildTasksStore()
    await this.loadTasks()
  },

  methods: {
    async loadTasks() {
      await Promise.all([
        this.loadActiveTasks(),
        this.loadCompletedTasks()
      ])
    },

    async loadActiveTasks() {
      this.activeTasks.loading = true
      try {
        // Загружаем невыполненные задания
        await this.store.fetchTasks({ is_completed: false })
        const notCompletedTasks = this.store.tasks

        // Загружаем возвращенные задания
        await this.store.fetchTasks({ is_completed: true, is_approved: false })
        const returnedTasks = this.store.tasks.filter(task => task.returned_at)

        // Объединяем задания
        this.activeTasks.tasks = [...notCompletedTasks, ...returnedTasks]
      } catch (err) {
        console.error('Error loading active tasks:', err)
        this.activeTasks.error = 'Не удалось загрузить активные задания'
      } finally {
        this.activeTasks.loading = false
      }
    },

    async loadCompletedTasks() {
      this.completedTasks.loading = true
      this.completedTasks.error = null

      try {
        const filters = { is_completed: true }

        if (this.completedFilter === 'pending') {
          filters.is_approved = false
        } else if (this.completedFilter === 'approved') {
          filters.is_approved = true
        }

        await this.store.fetchTasks(filters)
        // Фильтруем возвращенные задания из списка выполненных
        this.completedTasks.tasks = this.store.tasks.filter(task => !task.returned_at)
      } catch (err) {
        console.error('Error loading completed tasks:', err)
        this.completedTasks.error = 'Не удалось загрузить выполненные задания'
      } finally {
        this.completedTasks.loading = false
      }
    },

    formatDate(date) {
      if (!date) return ''
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(date))
    },

    async handleComplete(task) {
      try {
        this.completing = task.id
        await this.store.completeTask(task.id)
        await this.loadTasks()
      } catch (err) {
        console.error('Error completing task:', err)
      } finally {
        this.completing = null
      }
    }
  }
}
</script>