<template>
  <AuthForm />
</template>

<script>
import AuthForm from '~/components/auth/AuthForm.vue'

export default {
  name: 'AuthPage',
  middleware: ['guest'],
  components: {
    AuthForm
  }
}
</script>