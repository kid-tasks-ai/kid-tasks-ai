<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">
        {{ isLogin ? 'Вход' : 'Регистрация' }}
      </h2>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-700">Имя</label>
          <input
              v-model="formData.name"
              type="text"
              required
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="Введите ваше имя"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input
              v-model="formData.email"
              type="email"
              required
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="Введите ваш email"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Пароль</label>
          <input
              v-model="formData.password"
              type="password"
              required
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
              placeholder="Введите пароль"
          >
        </div>

        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>

        <button
            type="submit"
            class="w-full bg-blue-500 text-white rounded-md py-2 hover:bg-blue-600 transition-colors"
            :disabled="loading"
        >
          {{ loading ? 'Загрузка...' : (isLogin ? 'Войти' : 'Зарегистрироваться') }}
        </button>
      </form>

      <button
          @click="isLogin = !isLogin"
          class="mt-4 text-blue-500 hover:underline text-sm w-full text-center"
      >
        {{ isLogin ? 'Нет аккаунта? Зарегистрируйтесь' : 'Уже есть аккаунт? Войдите' }}
      </button>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const { setAuth } = useAuth()
const router = useRouter()

const isLogin = ref(true)
const error = ref('')
const loading = ref(false)
const formData = reactive({
  email: '',
  password: '',
  name: ''
})

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      const formBody = new FormData()
      formBody.append('username', formData.email)
      formBody.append('password', formData.password)

      const response = await $fetch('/api/v1/auth/login', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: formBody
      })

      if (response?.access_token) {
        setAuth(response.access_token, response.role)
        router.push(response.role === 'parent' ? '/parent' : '/child')
      }
    } else {
      const response = await $fetch('/api/v1/auth/register', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: {
          email: formData.email,
          password: formData.password,
          name: formData.name
        }
      })

      if (response?.id) {
        isLogin.value = true
        await handleSubmit()
      }
    }
  } catch (err) {
    error.value = err.data?.detail || 'Произошла ошибка при обработке запроса'
  } finally {
    loading.value = false
  }
}
</script>
