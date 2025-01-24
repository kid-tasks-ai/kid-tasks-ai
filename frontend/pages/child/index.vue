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
                  Назначено: {{ formatDate(task.assigned_at) }}
                </span>
              </div>
            </div>
            <UButton
                color="primary"
                :loading="completing === task.id"
                @click="handleComplete(task)"
            >
              Выполнено
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

          <!-- Фильтр для отображения одобренных/на проверке -->
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

<script lang="ts">
import { useChildTasksStore, type TaskAssignment } from '~/stores/childTasks'

definePageMeta({
  middleware: ['child']
})

export default {
  name: 'ChildTasksPage',
  layout: 'child',

  setup() {
    const store = useChildTasksStore()
    return { store }
  },

  data() {
    return {
      completing: null as number | null,
      completedFilter: null as null | 'pending' | 'approved',
      activeTasks: {
        tasks: [] as TaskAssignment[],
        loading: false,
        error: null as string | null
      },
      completedTasks: {
        tasks: [] as TaskAssignment[],
        loading: false,
        error: null as string | null
      }
    }
  },

  watch: {
    completedFilter() {
      this.loadCompletedTasks()
    }
  },

  async created() {
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
      this.activeTasks.error = null

      try {
        await this.store.fetchTasks({ is_completed: false })
        this.activeTasks.tasks = this.store.tasks.value
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
        const filters: Record<string, boolean> = { is_completed: true }

        if (this.completedFilter === 'pending') {
          filters.is_approved = false
        } else if (this.completedFilter === 'approved') {
          filters.is_approved = true
        }

        await this.store.fetchTasks(filters)
        this.completedTasks.tasks = this.store.tasks.value
      } catch (err) {
        console.error('Error loading completed tasks:', err)
        this.completedTasks.error = 'Не удалось загрузить выполненные задания'
      } finally {
        this.completedTasks.loading = false
      }
    },

    formatDate(date: string | null) {
      if (!date) return ''
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }).format(new Date(date))
    },

    async handleComplete(task: TaskAssignment) {
      try {
        this.completing = task.id
        await this.store.completeTask(task.id)
        await this.loadTasks() // Перезагружаем оба списка
      } catch (err) {
        console.error('Error completing task:', err)
      } finally {
        this.completing = null
      }
    }
  }
}
</script>