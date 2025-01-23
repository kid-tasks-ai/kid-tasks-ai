<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold">Шаблоны заданий</h1>
      <UButton
          color="primary"
          icon="i-heroicons-plus"
          @click="showCreateForm"
      >
        Создать шаблон
      </UButton>
    </div>

    <!-- Фильтры -->
    <UCard class="mb-6">
      <div class="flex gap-4 items-end">
        <UFormGroup label="Ребёнок" class="flex-1">
          <USelect
              v-model="filters.childId"
              :options="children"
              option-attribute="name"
              value-attribute="id"
              placeholder="Выберите ребёнка"
              @change="loadTemplates"
          />
        </UFormGroup>
        <UFormGroup label="Статус" class="flex-1">
          <USelect
              v-model="filters.status"
              :options="[
              { label: 'Все', value: null },
              { label: 'Активные', value: true },
              { label: 'Неактивные', value: false }
            ]"
              option-attribute="label"
              value-attribute="value"
              @change="loadTemplates"
          />
        </UFormGroup>
        <UButton
            icon="i-heroicons-x-mark"
            color="gray"
            variant="ghost"
            @click="resetFilters"
        >
          Сбросить
        </UButton>
      </div>
    </UCard>

    <!-- Список шаблонов -->
    <div v-if="templatesStore.loading.value" class="flex justify-center py-8">
      <UProgress />
    </div>

    <div v-else-if="templatesStore.error.value" class="mb-6">
      <UAlert
          :title="templatesStore.error.value"
          color="red"
          variant="soft"
      />
    </div>

    <div v-else>
      <!-- Пустое состояние -->
      <div v-if="templates.length === 0" class="mb-6">
        <UAlert
            title="Нет шаблонов"
            description="Создайте первый шаблон задания для ваших детей"
            icon="i-heroicons-information-circle"
        />
      </div>

      <!-- Список шаблонов -->
      <div v-else class="grid gap-4">
        <UCard v-for="template in templates" :key="template.id">
          <div class="flex justify-between">
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-medium">{{ template.title }}</h3>
                <UBadge
                    v-if="template.category"
                    color="gray"
                    variant="subtle"
                    size="sm"
                >
                  {{ template.category }}
                </UBadge>
                <UBadge
                    :color="template.is_active ? 'green' : 'gray'"
                    variant="subtle"
                    size="sm"
                >
                  {{ template.is_active ? 'Активен' : 'Неактивен' }}
                </UBadge>
              </div>
              <p class="text-gray-600">{{ template.description }}</p>
              <div class="flex gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-star" />
                  {{ template.points_value }} баллов
                </span>
                <span class="flex items-center gap-1">
                  <UIcon name="i-heroicons-clock" />
                  {{ getScheduleText(template) }}
                </span>
              </div>
            </div>
            <div class="flex items-start gap-2">
              <UButton
                  icon="i-heroicons-pencil-square"
                  color="gray"
                  variant="ghost"
                  @click="editTemplate(template)"
              />
              <UButton
                  icon="i-heroicons-trash"
                  color="red"
                  variant="ghost"
                  @click="confirmDelete(template)"
              />
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Модальное окно создания/редактирования -->
    <UModal
        :model-value="showForm"
        @close="closeForm"
    >
      <UCard>
        <template #header>
          <h3 class="text-lg font-medium">
            {{ editingTemplate ? 'Редактирование шаблона' : 'Новый шаблон' }}
          </h3>
        </template>
        <!-- Здесь будет форма -->
      </UCard>
    </UModal>
  </div>
</template>

<script lang="ts">
import { useChildrenStore } from '~/stores/children'
import { useTemplatesStore } from '~/stores/templates'
import type { Template } from '~/types/templates'

export default {
  name: 'TemplatesPage',
  layout: 'parent',
  middleware: ['parent'],

  setup() {
    const templatesStore = useTemplatesStore()
    return {
      templatesStore
    }
  },

  data() {
    return {
      children: [],

      filters: {
        childId: null as number | null,

        status: null as boolean | null
      },
      showForm: false,
      editingTemplate: null as Template | null,
      formLoading: false
    }
  },

  computed: {
    templates() {
      return this.templatesStore.templates.value
    }
  },

  async created() {
    try {
      await this.loadChildren()
      // Загружаем шаблоны только если есть выбранный ребенок
      if (this.children?.length) {
        this.filters.childId = this.children[0].id
        await this.loadTemplates()
      }
    } catch (err) {
      console.error('Error in created hook:', err)
    }
  },

  methods: {
    async loadChildren() {
      try {
        const store = useChildrenStore()
        await store.fetchChildren()
        this.children = store.children.value
      } catch (err) {
        console.error('Error loading children:', err)
      }
    },

    async loadTemplates() {
      try {
        await this.templatesStore.fetchTemplates(this.filters)
      } catch (err) {
        console.error('Error loading templates:', err)
      }
    },

    resetFilters() {
      this.filters = {
        childId: null,
        category: null,
        status: null
      }
      this.loadTemplates()
    },

    getScheduleText(template: Template) {
      const types = {
        once: 'Единоразово',
        daily: 'Ежедневно',
        weekly: 'Еженедельно'
      }
      return types[template.schedule_type] || template.schedule_type
    },

    showCreateForm() {
      this.editingTemplate = null
      this.showForm = true
    },

    editTemplate(template: Template) {
      this.editingTemplate = { ...template }
      this.showForm = true
    },

    closeForm() {
      if (!this.formLoading) {
        this.showForm = false
        this.editingTemplate = null
      }
    },

    async confirmDelete(template: Template) {
      if (await confirm(`Удалить шаблон "${template.title}"?`)) {
        try {
          await this.templatesStore.deleteTemplate(template.id)
        } catch (err) {
          console.error('Error deleting template:', err)
        }
      }
    }
  }
}
</script>