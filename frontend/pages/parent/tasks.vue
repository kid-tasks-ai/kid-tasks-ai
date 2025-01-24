<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Назначенные заданиями</h1>

    <!-- Фильтры -->
    <UCard class="mb-6">
      <div class="flex flex-wrap gap-4">
        <UFormGroup label="Ребёнок" class="flex-1">
          <USelect
              v-model="filters.childId"
              :options="children"
              option-attribute="name"
              value-attribute="id"
              placeholder="Выберите ребёнка"
              @change="loadAssignments"
          />
        </UFormGroup>
        <UFormGroup label="Статус выполнения" class="flex-1">
          <USelect
              v-model="filters.isCompleted"
              :options="completionStatuses"
              option-attribute="label"
              value-attribute="value"
              @change="loadAssignments"
          />
        </UFormGroup>
        <UFormGroup label="Статус проверки" class="flex-1">
          <USelect
              v-model="filters.isApproved"
              :options="approvalStatuses"
              option-attribute="label"
              value-attribute="value"
              @change="loadAssignments"
          />
        </UFormGroup>
        <div class="flex items-end">
          <UButton
              icon="i-heroicons-x-mark"
              color="gray"
              variant="ghost"
              @click="resetFilters"
          >
            Сбросить
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Список заданий -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress />
    </div>

    <div v-else-if="error" class="mb-6">
      <UAlert
          :title="error"
          color="red"
          variant="soft"
      />
    </div>

    <div v-else>
      <!-- Пустое состояние -->
      <div v-if="!filters.childId" class="mb-6">
        <UAlert
            title="Выберите ребёнка"
            description="Для просмотра заданий выберите ребёнка"
            icon="i-heroicons-information-circle"
        />
      </div>
      <div v-else-if="assignments.length === 0" class="mb-6">
        <UAlert
            title="Нет заданий"
            description="У выбранного ребёнка пока нет заданий"
            icon="i-heroicons-information-circle"
        />
      </div>

      <!-- Список заданий -->
      <div v-else class="grid gap-4">
        <UCard v-for="assignment in assignments" :key="assignment.id">
          <div class="flex justify-between">
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-medium">{{ assignment.template.title }}</h3>
                <UBadge
                    :color="getStatusColor(assignment)"
                    variant="subtle"
                    size="sm"
                >
                  {{ getStatusText(assignment) }}
                </UBadge>
              </div>
              <p class="text-gray-600">{{ assignment.template.description }}</p>
              <div class="flex flex-wrap gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-star" />
                  {{ assignment.points_value }} баллов
                </span>
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-calendar" />
                  Назначено: {{ formatDate(assignment.assigned_at) }}
                </span>
                <span v-if="assignment.completed_at" class="flex items-center gap-1">
                  <UIcon name="i-heroicons-check-circle" />
                  Выполнено: {{ formatDate(assignment.completed_at) }}
                </span>
                <span v-if="assignment.approved_at" class="flex items-center gap-1">
                  <UIcon name="i-heroicons-check-badge" />
                  Проверено: {{ formatDate(assignment.approved_at) }}
                </span>
              </div>
            </div>
            <div class="flex items-start gap-2">
              <UButton
                  v-if="assignment.is_completed && !assignment.is_approved"
                  icon="i-heroicons-check"
                  color="green"
                  variant="soft"
                  @click="approveAssignment(assignment.id)"
              >
                Принять
              </UButton>
              <UButton
                  v-if="!assignment.is_completed"
                  icon="i-heroicons-arrow-path"
                  color="red"
                  variant="soft"
                  @click="returnAssignment(assignment.id)"
              >
                Вернуть
              </UButton>
              <UButton
                  icon="i-heroicons-trash"
                  color="red"
                  variant="ghost"
                  @click="deleteAssignment(assignment.id)"
                  :disabled="assignment.is_approved"
                  class="ml-2"
              >
                Удалить
              </UButton>
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <UModal v-model="showDeleteModal">
      <div class="p-4">
        <h3 class="text-lg font-medium mb-4">Подтверждение удаления</h3>
        <p class="text-gray-600 mb-6">
          Вы действительно хотите удалить это задание? Это действие нельзя будет отменить.
        </p>
        <div class="flex justify-end gap-2">
          <UButton
              variant="ghost"
              @click="showDeleteModal = false"
          >
            Отмена
          </UButton>
          <UButton
              color="red"
              variant="solid"
              :loading="deleteLoading"
              @click="confirmDelete"
          >
            Удалить
          </UButton>
        </div>
      </div>
    </UModal>
  </div>
</template>

<script>
import { useChildrenStore } from '~/stores/children'
import { useAssignmentsStore } from '~/stores/assignments'

export default {
  name: 'TasksPage',
  layout: 'parent',
  middleware: ['parent'],

  data() {
    return {
      filters: {
        childId: null,
        isCompleted: undefined,
        isApproved: undefined
      },
      completionStatuses: [
        { label: 'Все', value: undefined },
        { label: 'Выполненные', value: true },
        { label: 'Не выполненные', value: false }
      ],
      approvalStatuses: [
        { label: 'Все', value: undefined },
        { label: 'Принятые', value: true },
        { label: 'Не принятые', value: false }
      ],
      assignments: [],
      loading: false,
      error: null,
      showDeleteModal: false,
      deleteLoading: false,
      assignmentToDelete: null
    }
  },

  computed: {
    children() {
      const childrenStore = useChildrenStore()
      return childrenStore.children.value
    }
  },

  async created() {
    await this.loadInitialData()
  },

  methods: {
    async loadAssignments() {
      if (!this.filters.childId) return

      try {
        this.loading = true
        const assignmentsStore = useAssignmentsStore()
        await assignmentsStore.fetchAssignments(this.filters)
        this.assignments = assignmentsStore.assignments.value
        this.error = null
      } catch (err) {
        console.error('Error loading assignments:', err)
        this.error = 'Не удалось загрузить задания'
      } finally {
        this.loading = false
      }
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getStatusColor(assignment) {
      if (assignment.is_approved) return 'green'
      if (assignment.is_completed) return 'yellow'
      return 'blue'
    },

    getStatusText(assignment) {
      if (assignment.is_approved) return 'Принято'
      if (assignment.is_completed) return 'На проверке'
      return 'В работе'
    },

    resetFilters() {
      this.filters = {
        childId: this.filters.childId,
        isCompleted: undefined,
        isApproved: undefined
      }
      this.loadAssignments()
    },

    async approveAssignment(assignmentId) {
      try {
        this.loading = true
        const assignmentsStore = useAssignmentsStore()
        await assignmentsStore.approveAssignment(assignmentId)
        await this.loadAssignments()
      } catch (err) {
        console.error('Error approving assignment:', err)
        this.error = 'Не удалось одобрить задание'
      } finally {
        this.loading = false
      }
    },

    async returnAssignment(assignmentId) {
      // TODO: Implement return assignment functionality
      console.log('Return assignment:', assignmentId)
    },

    async loadInitialData() {
      try {
        const childrenStore = useChildrenStore()
        await childrenStore.fetchChildren()
        if (this.children.length > 0) {
          this.filters.childId = this.children[0].id
          await this.loadAssignments()
        }
      } catch (err) {
        console.error('Error loading initial data:', err)
        this.error = 'Не удалось загрузить данные'
      }
    },

    // Новые методы для удаления
    deleteAssignment(assignmentId) {
      this.assignmentToDelete = assignmentId
      this.showDeleteModal = true
    },

    async confirmDelete() {
      if (!this.assignmentToDelete) return

      try {
        this.deleteLoading = true
        const assignmentsStore = useAssignmentsStore()
        await assignmentsStore.deleteAssignment(this.assignmentToDelete)

        const { $notify } = useNuxtApp()
        $notify.success('Задание удалено')

        // Закрываем модальное окно и обновляем список
        this.showDeleteModal = false
        this.assignmentToDelete = null
        await this.loadAssignments()

      } catch (err) {
        console.error('Error deleting assignment:', err)

        // Определяем текст ошибки
        let errorMessage = 'Не удалось удалить задание'
        if (err.response?.status === 400) {
          errorMessage = 'Нельзя удалить одобренное задание'
        } else if (err.response?.status === 404) {
          errorMessage = 'Задание не найдено'
        } else if (err.response?.status === 403) {
          errorMessage = 'У вас нет прав на удаление задания'
        }

        // Показываем ошибку пользователю
        this.error = errorMessage

        // Если это критическая ошибка - закрываем модальное окно
        if (err.response?.status === 404) {
          this.showDeleteModal = false
          this.assignmentToDelete = null
          await this.loadAssignments() // Обновляем список на случай рассинхронизации
        }
      } finally {
        this.deleteLoading = false
      }
    }
  }
}
</script>