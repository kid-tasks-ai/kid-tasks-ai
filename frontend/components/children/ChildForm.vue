<!-- components/children/ChildForm.vue -->
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
          :disabled="isEditing"
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
      <template v-if="isEditing" #help>
        <span class="text-sm text-gray-500">Оставьте пустым, чтобы не менять пароль</span>
      </template>
    </UFormGroup>

    <UFormGroup label="Возраст" required>
      <UInput
          v-model="form.age"
          type="number"
          :min="1"
          :max="18"
          placeholder="Введите возраст"
          :error="errors.age"
          required
      />
    </UFormGroup>

    <UFormGroup label="Пол" required class="mb-4">
      <div class="flex gap-6">
        <label class="flex items-center gap-2 cursor-pointer">
          <URadio
              v-model="form.gender"
              value="male"
              name="gender"
              required
          />
          <UIcon
              name="i-heroicons-user-circle"
              class="w-5 h-5 text-blue-500"
          />
          <span>Мальчик</span>
        </label>

        <label class="flex items-center gap-2 cursor-pointer">
          <URadio
              v-model="form.gender"
              value="female"
              name="gender"
              required
          />
          <UIcon
              name="i-heroicons-user"
              class="w-5 h-5 text-pink-500"
          />
          <span>Девочка</span>
        </label>
      </div>
      <p v-if="errors.gender" class="mt-1 text-sm text-red-500">{{ errors.gender }}</p>
    </UFormGroup>

    <UFormGroup label="Интересы">
      <UTextarea
          v-model="form.interests"
          placeholder="Опишите интересы ребенка"
          :error="errors.interests"
          :rows="3"
      />
    </UFormGroup>

    <UFormGroup label="Предпочтения">
      <UTextarea
          v-model="form.preferences"
          placeholder="Укажите предпочтения ребенка"
          :error="errors.preferences"
          :rows="3"
      />
    </UFormGroup>

    <div class="flex justify-end gap-2 mt-6">
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

<script>
export default {
  name: 'ChildForm',

  props: {
    initialData: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      required: true
    }
  },

  emits: ['submit', 'cancel'],

  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        age: 0,
        gender: '',
        interests: '',
        preferences: ''
      },
      genderOptions: [
        { value: 'male', label: 'Мальчик', icon: 'i-heroicons-user-circle' },
        { value: 'female', label: 'Девочка', icon: 'i-heroicons-user-circle' }
      ],
      errors: {}
    }
  },

  computed: {
    isEditing() {
      return Boolean(this.initialData?.id)
    },
    submitButtonText() {
      return this.isEditing ? 'Сохранить' : 'Добавить'
    }
  },

  mounted() {
    this.initForm()
  },

  watch: {
    'initialData.id'(newId, oldId) {
      if (newId !== oldId) {
        this.initForm()
      }
    }
  },

  methods: {
    initForm() {
      this.form = {
        name: '',
        email: '',
        password: '',
        age: 0,
        interests: '',
        preferences: '',
        ...(this.initialData || {})
      }
      this.errors = {}
    },

    handleSubmit() {
      const formData = { ...this.form }

      // Преобразуем age в число
      if (formData.age) {
        formData.age = parseInt(String(formData.age))
      }

      // При редактировании не отправляем email и пустой пароль
      if (this.isEditing) {
        delete formData.email
        if (!formData.password) {
          delete formData.password
        }
      }

      // Очищаем пустые строки
      Object.entries(formData).forEach(([key, value]) => {
        if (value === '') {
          formData[key] = null
        }
      })

      this.$emit('submit', formData)
    }
  }
}
</script>