# pages/parent/children.vue
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление профилями детей</h1>
    <UCard class="mb-6">
      <template #header>
        <h2 class="text-lg font-medium">Профили детей</h2>
      </template>

      <div class="space-y-4">
        <!-- Список детей будет здесь -->
        <p class="text-gray-500">Список профилей пока пуст</p>
      </div>

      <template #footer>
        <UButton
            color="primary"
            @click="showAddChildForm = true"
        >
          Добавить ребенка
        </UButton>
      </template>
    </UCard>
  </div>
</template>

<script setup>
const showAddChildForm = ref(false)

definePageMeta({
  layout: 'parent',
  middleware: ['parent']
})
</script>
