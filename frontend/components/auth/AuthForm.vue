<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <UCard class="w-full max-w-md">
      <template #header>
        <h2 class="text-2xl font-bold text-center">
          {{ isLogin ? 'Вход' : 'Регистрация' }}
        </h2>
      </template>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <UFormGroup v-if="!isLogin" label="Имя" required>
          <UInput
              v-model="formData.name"
              placeholder="Введите ваше имя"
          />
        </UFormGroup>

        <UFormGroup label="Email" required>
          <UInput
              v-model="formData.email"
              type="email"
              placeholder="Введите ваш email"
          />
        </UFormGroup>

        <UFormGroup label="Пароль" required>
          <UInput
              v-model="formData.password"
              type="password"
              placeholder="Введите пароль"
          />
        </UFormGroup>

        <UAlert
            v-if="error"
            :description="error"
            color="red"
            variant="soft"
            class="mt-4"
        />

        <UButton
            type="submit"
            block
            color="primary"
            :loading="loading"
        >
          {{ submitButtonText }}
        </UButton>
      </form>

      <template #footer>
        <UButton
            variant="ghost"
            color="gray"
            block
            @click="toggleAuthMode"
        >
          {{ toggleButtonText }}
        </UButton>
      </template>
    </UCard>
  </div>
</template>

<script>
import { useAuthStore } from '~/stores/auth'

export default {
  name: 'AuthForm',

  data() {
    return {
      isLogin: true,
      error: '',
      loading: false,
      formData: {
        email: '',
        password: '',
        name: ''
      }
    }
  },

  computed: {
    submitButtonText() {
      if (this.loading) return 'Загрузка...'
      return this.isLogin ? 'Войти' : 'Зарегистрироваться'
    },
    toggleButtonText() {
      return this.isLogin
          ? 'Нет аккаунта? Зарегистрируйтесь'
          : 'Уже есть аккаунт? Войдите'
    }
  },

  methods: {
    toggleAuthMode() {
      this.isLogin = !this.isLogin
      this.error = ''
    },

    async handleSubmit() {
      this.error = ''
      this.loading = true
      const auth = useAuthStore()

      try {
        if (this.isLogin) {
          const role = await auth.login(this.formData.email, this.formData.password)
          this.$router.push(role === 'parent' ? '/parent' : '/child')
        } else {
          await auth.register(this.formData)
          this.isLogin = true
          this.formData.password = ''
          this.formData.name = ''
        }
      } catch (err) {
        console.error('Auth error:', err)
        this.error = err.data?.detail || 'Произошла ошибка при обработке запроса'
      } finally {
        this.loading = false
      }
    }
  },
  setup() {
    const auth = useAuthStore()
    return { auth }
  },
}
</script>