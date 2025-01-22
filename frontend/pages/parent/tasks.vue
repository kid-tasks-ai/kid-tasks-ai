<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Управление заданиями</h1>

    <!-- Карточка для генерации заданий -->
    <UCard class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium">Генерация заданий</h3>
          <UButton
              icon="i-heroicons-sparkles"
              label="Создать новые задания"
              @click="generateTasks"
              :loading="isGenerating"
          />
        </div>
      </template>
      <!-- Здесь будут настройки генерации -->
      <p class="text-gray-500">Настройте параметры генерации заданий для ваших детей</p>
    </UCard>

    <!-- Список активных заданий -->
    <UCard class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium">Активные задания</h3>
          <UButton
              icon="i-heroicons-funnel"
              variant="ghost"
              @click="toggleFilters"
          />
        </div>
      </template>

      <!-- Заглушка для списка -->
      <UAlert
          title="Нет активных заданий"
          description="Сгенерируйте новые задания или создайте их вручную"
          icon="i-heroicons-information-circle"
      />
    </UCard>

    <!-- История заданий -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium">История заданий</h3>
        </div>
      </template>

      <!-- Заглушка для истории -->
      <p class="text-gray-500">История выполненных заданий появится здесь</p>
    </UCard>
  </div>
</template>

<script>
export default {
  name: 'TasksPage',
  layout: 'parent',
  middleware: ['parent'],
  data() {
    return {
      isGenerating: false,
      showFilters: false
    }
  },

  methods: {
    generateTasks() {
      this.isGenerating = true
      // TODO: Implement task generation
      setTimeout(() => {
        this.isGenerating = false
      }, 2000)
    },

    toggleFilters() {
      this.showFilters = !this.showFilters
    }
  }
}
</script>
