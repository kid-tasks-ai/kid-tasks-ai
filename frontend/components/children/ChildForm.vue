<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <UFormGroup label="Имя" required>
      <UInput
          v-model="form.name"
          placeholder="Введите имя ребенка"
          :error="errors.name"
          required
      />
    </UFormGroup>

    <UFormGroup label="Email" required>
      <UInput
          v-model="form.email"
          type="email"
          placeholder="Введите email"
          :error="errors.email"
          required
      />
    </UFormGroup>

    <UFormGroup label="Пароль" :required="!isEditing">
      <UInput
          v-model="form.password"
          type="password"
          placeholder="Введите пароль"
          :error="errors.password"
          :required="!isEditing"
      />
    </UFormGroup>

    <UFormGroup label="Возраст" required>
      <UInput
          v-model="form.age"
          type="number"
          min="1"
          max="18"
          placeholder="Введите возраст"
          :error="errors.age"
          required
      />
    </UFormGroup>

    <UFormGroup label="Интересы">
      <UTextarea
          v-model="form.interests"
          placeholder="Опишите интересы ребенка"
          :error="errors.interests"
      />
    </UFormGroup>

    <UFormGroup label="Предпочтения">
      <UTextarea
          v-model="form.preferences"
          placeholder="Укажите предпочтения ребенка"
          :error="errors.preferences"
      />
    </UFormGroup>

    <div class="flex justify-end gap-2 mt-4">
      <UButton
          type="button"
          variant="ghost"
          @click="$emit('cancel')"
      >
        Отмена
      </UButton>
      <UButton
          type="submit"
          color="primary"
          :loading="loading"
          class="text-white"
      >
        {{ submitButtonText }}
      </UButton>
    </div>
  </form>
</template>

<script setup>
const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

// Исправленное вычисляемое свойство
const isEditing = computed(() => Boolean(props.initialData?.id))
const submitButtonText = computed(() => isEditing.value ? 'Сохранить' : 'Добавить')

const form = ref({
  name: '',
  email: '',
  password: '',
  age: null,
  interests: '',
  preferences: '',
  ...(props.initialData || {})
})

const errors = ref({})

// Сбрасываем форму при инициализации
onMounted(() => {
  resetForm()
})

function handleSubmit() {
  const formData = {...form.value}

  // Преобразуем age в число
  if (formData.age) {
    formData.age = parseInt(formData.age)
  }

  // Удаляем пустой пароль при редактировании
  if (isEditing.value && !formData.password) {
    delete formData.password
  }

  // Очищаем пустые строки
  Object.keys(formData).forEach(key => {
    if (formData[key] === '') {
      formData[key] = null
    }
  })

  emit('submit', formData)
}

function resetForm() {
  form.value = {
    name: '',
    email: '',
    password: '',
    age: null,
    interests: '',
    preferences: '',
    ...(props.initialData || {})
  }
  errors.value = {}
}

// Исправленный watch с проверкой на null
watch(() => props.initialData, (newData) => {
  form.value = {
    name: '',
    email: '',
    password: '',
    age: '',
    interests: '',
    preferences: '',
    ...(newData || {})
  }
}, {deep: true})
</script>