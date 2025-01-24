<template>
  <AuthForm />
</template>

<script>
import AuthForm from '~/components/auth/AuthForm.vue'

definePageMeta({
  middleware: ['guest']
})

export default {
  name: 'AuthPage',
  components: {
    AuthForm
  }
}
</script>