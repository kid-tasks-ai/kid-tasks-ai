<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление профилями детей</h1>

    <!-- Общее сообщение об ошибке -->
    <UAlert
        v-if="pageError"
        title="Ошибка"
        :description="pageError"
        color="red"
        variant="soft"
        class="mb-4"
        :icon="false"
    >
      <template #footer>
        <div class="flex justify-end">
          <UButton
              variant="ghost"
              color="red"
              size="sm"
              @click="pageError = null"
          >
            Закрыть
          </UButton>
        </div>
      </template>
    </UAlert>

    <!-- Карточка со списком детей -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress />
    </div>

    <div v-else>
      <div v-if="children.length === 0" class="mb-6">
        <UAlert
            title="Нет профилей"
            description="У вас пока нет добавленных профилей детей"
            icon="i-heroicons-information-circle"
        />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <ChildCard
            v-for="child in children"
            :key="child.id"
            :child="child"
            @edit="editChild(child)"
            @delete="deleteChild(child.id)"
        />
      </div>
    </div>

    <!-- Кнопка добавления -->
    <UButton
        color="primary"
        @click="showAddForm"
        :disabled="loading"
    >
      Добавить ребенка
    </UButton>

    <UModal
        :model-value="showForm"
        @update:model-value="handleModelUpdate"
    >
      <template #default>
        <div class="p-4">
          <h2 class="text-lg font-medium mb-4">
            {{ editingChild ? 'Редактировать профиль' : 'Добавить ребенка' }}
          </h2>

          <!-- Сообщение об ошибке в модальном окне -->
          <UAlert
              v-if="formError"
              title="Ошибка"
              :description="formError"
              color="red"
              variant="soft"
              class="mb-4"
          />

          <ChildForm
              :initial-data="editingChild || {}"
              :loading="formLoading"
              @submit="handleSubmit"
              @cancel="handleModalClose"
          />
        </div>
      </template>
    </UModal>
  </div>
</template>

<script>
import { useChildrenStore } from '~/stores/children'
import ChildCard from '~/components/children/ChildCard.vue'
import ChildForm from '~/components/children/ChildForm.vue'

export default {
  name: 'ChildrenPage',
  layout: 'parent',
  middleware: ['parent'],
  components: {
    ChildCard,
    ChildForm
  },

  data() {
    return {
      showForm: false,
      editingChild: null,
      formLoading: false,
      formError: null,
      pageError: null, // добавляем для общих ошибок страницы
    }
  },

  computed: {
    children() {
      const store = useChildrenStore()
      return store.children.value
    },
    loading() {
      const store = useChildrenStore()
      return store.loading.value
    }
  },

  async created() {
    const store = useChildrenStore()
    try {
      await store.fetchChildren()
    } catch (err) {
      console.error('Error fetching children:', err)
      this.pageError = 'Не удалось загрузить список детей. Попробуйте обновить страницу.'
    }
  },

  methods: {
    // Обновим существующие методы для сброса pageError
    showAddForm() {
      this.formError = null
      this.pageError = null
      this.editingChild = null
      this.showForm = true
    },

    editChild(child) {
      this.formError = null
      this.pageError = null
      this.editingChild = {...child}
      this.showForm = true
    },

    handleModalClose() {
      this.showForm = false
      this.editingChild = null
      this.formError = null
      // pageError не сбрасываем здесь, так как это ошибка страницы
    },

    async deleteChild(id) {
      if (confirm('Вы уверены, что хотите удалить этот профиль?')) {
        try {
          const store = useChildrenStore()
          await store.deleteChild(id)
          this.pageError = null // Сбрасываем ошибку при успехе
        } catch (err) {
          console.error('Error deleting child:', err)
          this.pageError = 'Не удалось удалить профиль. Попробуйте еще раз.'
        }
      }
    },

    async handleSubmit(formData) {
      try {
        this.formLoading = true
        this.formError = null
        const store = useChildrenStore()

        if (this.editingChild?.id) {
          await store.updateChild(this.editingChild.id, formData)
        } else {
          await store.createChild(formData)
        }

        this.handleModalClose() // Закрываем только при успешном сохранении
      } catch (err) {
        console.error('Error submitting form:', err)
        this.formError = err?.data?.detail || 'Произошла ошибка при сохранении данных'
      } finally {
        this.formLoading = false
      }
    },

    handleModelUpdate(value) {
      if (!value) { // Если модальное окно закрывается
        // Проверяем, нет ли ошибок и не идет ли загрузка
        if (!this.formError && !this.formLoading) {
          this.handleModalClose()
        }
      } else {
        this.showForm = value
      }
    }
  }
}
</script>