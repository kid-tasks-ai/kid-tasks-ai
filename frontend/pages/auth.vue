<template>
  <AuthForm />
</template>

<script setup>
import AuthForm from '~/components/auth/AuthForm.vue'

definePageMeta({
  middleware: ['guest']
})
</script>