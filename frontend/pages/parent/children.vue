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
    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-lg w-full">
        <h2 class="text-lg font-medium mb-4">
          {{ editingChild ? 'Редактировать профиль' : 'Добавить ребенка' }}
        </h2>
        <ChildForm
            :initial-data="editingChild || {}"
            :loading="formLoading"
            @submit="handleSubmit"
            @cancel="closeForm"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useChildren } from '~/composables/useChildren'
import ChildCard from '~/components/children/ChildCard.vue'
import ChildForm from '~/components/children/ChildForm.vue'

definePageMeta({
  layout: 'parent',
  middleware: ['parent']
})

// Состояние
const showForm = ref(false)
const editingChild = ref(null)
const formLoading = ref(false)

// Отслеживаем изменение состояния модального окна
watch(showForm, (newValue) => {
  console.log('Modal state changed:', newValue)
})

// Получаем методы из composable
const {
  children,
  loading,
  error,
  fetchChildren,
  createChild,
  updateChild,
  deleteChild: removeChild
} = useChildren()

// Методы
function showAddForm() {
  console.log('Opening add form modal')
  editingChild.value = null
  showForm.value = true
}

function editChild(child) {
  editingChild.value = {...child} // Создаем копию объекта
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingChild.value = null
}

async function handleSubmit(formData) {
  try {
    formLoading.value = true
    console.log('Submitting form data:', formData)

    if (editingChild.value?.id) {
      console.log('Updating child:', editingChild.value.id)
      await updateChild(editingChild.value.id, formData)
    } else {
      console.log('Creating new child')
      await createChild(formData)
    }

    await fetchChildren() // Обновляем список после успешного действия
    showForm.value = false // Закрываем модальное окно
    editingChild.value = null // Сбрасываем редактируемый профиль
  } catch (err) {
    console.error('Error submitting form:', err)
    // Можно добавить отображение ошибки пользователю
  } finally {
    formLoading.value = false
  }
}

async function deleteChild(id) {
  if (confirm('Вы уверены, что хотите удалить этот профиль?')) {
    try {
      await removeChild(id)
      await fetchChildren() // Обновляем список после удаления
    } catch (err) {
      console.error('Error deleting child:', err)
    }
  }
}

// Загружаем данные при монтировании
onMounted(() => {
  fetchChildren()
})
</script>