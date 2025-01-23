<!-- pages/parent/templates.vue -->
<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold">Шаблоны заданий</h1>
      <div class="flex gap-3">
        <!-- Генератор задач -->
        <UButton
            color="purple"
            variant="solid"
            icon="i-heroicons-sparkles"
            :loading="isGenerating"
            :disabled="!filters.childId"
            @click="openGenerator"
            class="relative group"
        >
          <div class="flex items-center gap-2">
            <span>AI Генератор</span>
            <div class="absolute inset-0 rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-0 group-hover:opacity-20 transition-opacity"></div>
          </div>
        </UButton>

        <!-- Обычное добавление -->
        <UButton
            color="primary"
            icon="i-heroicons-plus"
            @click="showCreateForm"
            :disabled="!filters.childId"
        >
          Добавить шаблон
        </UButton>
      </div>
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
      <div v-if="!filters.childId" class="mb-6">
        <UAlert
            title="Выберите ребёнка"
            description="Для просмотра шаблонов заданий выберите ребёнка"
            icon="i-heroicons-information-circle"
        />
      </div>
      <div v-else-if="templates.length === 0" class="mb-6">
        <UAlert
            title="Нет шаблонов"
            description="Создайте первый шаблон задания для вашего ребёнка"
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
        :prevent-close="formLoading"
    >
      <template #default>
        <div class="p-4">
          <h2 class="text-lg font-medium mb-4">
            {{ editingTemplate ? 'Редактирование шаблона' : 'Новый шаблон' }}
          </h2>

          <TemplateForm
              :initial-data="editingTemplate || {}"
              :child-id="filters.childId"
              :loading="formLoading"
              @submit="handleFormSubmit"
              @cancel="handleModalClose"
          />
        </div>
      </template>
    </UModal>
  </div>
</template>

<script>
import { useChildrenStore } from '~/stores/children'
import { useTemplatesStore } from '~/stores/templates'
import TemplateForm from '~/components/tasks/TemplateForm.vue'

export default {
  name: 'TemplatesPage',
  layout: 'parent',
  middleware: ['parent'],

  components: {
    TemplateForm
  },

  setup() {
    const templatesStore = useTemplatesStore()
    return {
      templatesStore
    }
  },

  data() {
    return {
      filters: {
        childId: null,
        status: null
      },
      showForm: false,
      editingTemplate: null,
      formLoading: false,
      templates: [],
      children: [],
      isGenerating: false
    }
  },

  async created() {
    await this.loadChildren()
  },

  methods: {
    async loadTemplates() {
      try {
        if (!this.filters.childId) {
          this.templates = []
          return
        }

        await this.templatesStore.fetchTemplates({
          childId: this.filters.childId,
          status: this.filters.status !== null ? String(this.filters.status) : null
        })

        this.templates = this.templatesStore.templates.value
      } catch (err) {
        console.error('Error loading templates:', err)
      }
    },

    async loadChildren() {
      try {
        const store = useChildrenStore()
        await store.fetchChildren()
        this.children = store.children.value
        if (this.children.length > 0) {
          this.filters.childId = this.children[0].id
          await this.loadTemplates()
        }
      } catch (err) {
        console.error('Error loading children:', err)
      }
    },

    resetFilters() {
      this.filters.status = null
      this.loadTemplates()
    },

    getScheduleText(template) {
      const types = {
        once: 'Единоразово',
        daily: 'Ежедневно',
        weekly: 'Еженедельно'
      }
      return types[template.schedule_type] || template.schedule_type
    },

    showCreateForm() {
      if (!this.filters.childId) {
        return
      }
      this.editingTemplate = null
      this.showForm = true
    },

    editTemplate(template) {
      this.editingTemplate = { ...template }
      this.showForm = true
    },

    handleModalClose() {
      if (!this.formLoading) {
        this.showForm = false
        this.editingTemplate = null
      }
    },

    async confirmDelete(template) {
      if (await confirm(`Удалить шаблон "${template.title}"?`)) {
        try {
          await this.templatesStore.deleteTemplate(template.id)
          await this.loadTemplates()
        } catch (err) {
          console.error('Error deleting template:', err)
        }
      }
    },

    async handleFormSubmit(formData) {
      try {
        this.formLoading = true

        if (this.editingTemplate?.id) {
          await this.templatesStore.updateTemplate(this.editingTemplate.id, formData)
        } else {
          await this.templatesStore.createTemplate(formData)
        }

        await this.loadTemplates()
        this.showForm = false
        this.editingTemplate = null
      } catch (err) {
        console.error('Error saving template:', err)
      } finally {
        this.formLoading = false
      }
    },
    async openGenerator() {
      if (!this.filters.childId) return;
      // TODO: Здесь будет открываться модальное окно генератора
      this.isGenerating = true;
      try {
        // Заглушка для демонстрации анимации загрузки
        await new Promise(resolve => setTimeout(resolve, 1000));
        // TODO: Реализовать генерацию
      } finally {
        this.isGenerating = false;
      }
    }
  }
}
</script>