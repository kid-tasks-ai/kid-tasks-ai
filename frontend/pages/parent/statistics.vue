<!-- pages/parent/statistics.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Статистика</h1>

    <!-- Общая статистика -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-academic-cap" class="text-blue-500" />
            <h3 class="text-lg font-medium">Выполненные задания</h3>
          </div>
        </template>
        <p class="text-3xl font-bold text-gray-900">{{ completedTasks }}</p>
        <p class="text-sm text-gray-500">за последние 30 дней</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-gift" class="text-purple-500" />
            <h3 class="text-lg font-medium">Полученные награды</h3>
          </div>
        </template>
        <p class="text-3xl font-bold text-gray-900">{{ claimedRewards }}</p>
        <p class="text-sm text-gray-500">за последние 30 дней</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-star" class="text-yellow-500" />
            <h3 class="text-lg font-medium">Баланс баллов</h3>
          </div>
        </template>
        <p class="text-3xl font-bold text-gray-900">{{ totalPoints }}</p>
        <p class="text-sm text-gray-500">суммарно у всех детей</p>
      </UCard>
    </div>

    <!-- График активности -->
    <UCard class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium">График активности</h3>
          <USelect
              v-model="selectedPeriod"
              :options="periods"
              option-attribute="label"
              class="w-40"
          />
        </div>
      </template>
      <!-- Здесь будет график -->
      <div class="h-64 flex items-center justify-center bg-gray-50">
        <p class="text-gray-500">График в разработке</p>
      </div>
    </UCard>

    <!-- Таблица последних действий -->
    <UCard>
      <template #header>
        <h3 class="text-lg font-medium">Последние действия</h3>
      </template>
      <UTable
          :columns="columns"
          :rows="activities"
          :loading="loading"
      >
        <template #date-data="{ row }">
          {{ formatDate(row.date) }}
        </template>
        <template #type-data="{ row }">
          <UBadge
              :color="getActivityColor(row.type)"
              :variant="row.type === 'task' ? 'solid' : 'subtle'"
          >
            {{ getActivityLabel(row.type) }}
          </UBadge>
        </template>
      </UTable>
    </UCard>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'parent',
  middleware: ['parent']
})

// Состояние и константы
const completedTasks = ref(12)
const claimedRewards = ref(5)
const totalPoints = ref(450)
const selectedPeriod = ref('month')
const loading = ref(false)

// Опции для выбора периода
const periods = [
  { value: 'week', label: 'Неделя' },
  { value: 'month', label: 'Месяц' },
  { value: 'year', label: 'Год' }
]

// Конфигурация таблицы
const columns = [
  {
    key: 'date',
    label: 'Дата'
  },
  {
    key: 'child',
    label: 'Ребёнок'
  },
  {
    key: 'type',
    label: 'Тип'
  },
  {
    key: 'description',
    label: 'Описание'
  }
]

// Демо-данные для таблицы
const activities = [
  {
    date: new Date('2025-01-20'),
    child: 'Анна',
    type: 'task',
    description: 'Выполнено задание "Прочитать главу книги"'
  },
  {
    date: new Date('2025-01-19'),
    child: 'Михаил',
    type: 'reward',
    description: 'Получена награда "Поход в кино"'
  },
  // Добавьте больше демо-записей при необходимости
]

// Вспомогательные функции
function formatDate(date) {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

function getActivityColor(type) {
  return type === 'task' ? 'blue' : 'purple'
}

function getActivityLabel(type) {
  return type === 'task' ? 'Задание' : 'Награда'
}
</script>