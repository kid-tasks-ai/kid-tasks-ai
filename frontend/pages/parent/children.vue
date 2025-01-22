<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление профилями детей</h1>

    <!-- Сообщение об ошибке -->
    <UAlert
        v-if="error"
        title="Ошибка"
        :description="error"
        color="red"
        variant="soft"
        class="mb-4"
    />

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

    <!-- Модальное окно формы -->
    <UModal v-model="showForm">
      <template #default>
        <h2 class="text-lg font-medium mb-4">
          {{ editingChild ? 'Редактировать профиль' : 'Добавить ребенка' }}
        </h2>
        <ChildForm
            :initial-data="editingChild || {}"
            :loading="formLoading"
            @submit="handleSubmit"
        />
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
      formLoading: false
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
    },
    error() {
      const store = useChildrenStore()
      return store.error.value
    }
  },

  async created() {
    const store = useChildrenStore()
    await store.fetchChildren()
  },

  methods: {
    showAddForm() {
      this.editingChild = null
      this.showForm = true
    },

    editChild(child) {
      this.editingChild = {...child}
      this.showForm = true
    },

    async deleteChild(id) {
      if (confirm('Вы уверены, что хотите удалить этот профиль?')) {
        try {
          const store = useChildrenStore()
          await store.deleteChild(id)
        } catch (err) {
          console.error('Error deleting child:', err)
        }
      }
    },

    async handleSubmit(formData) {
      try {
        this.formLoading = true
        const store = useChildrenStore()

        if (this.editingChild?.id) {
          await store.updateChild(this.editingChild.id, formData)
        } else {
          await store.createChild(formData)
        }

        this.showForm = false
        this.editingChild = null
      } catch (err) {
        console.error('Error submitting form:', err)
      } finally {
        this.formLoading = false
      }
    }
  }
}
</script>
