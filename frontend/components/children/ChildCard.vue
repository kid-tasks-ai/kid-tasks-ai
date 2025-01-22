<template>
  <UCard>
    <template #header>
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-medium">{{ child.name }}</h3>
        <span class="text-sm text-gray-500">{{ child.age }} лет</span>
      </div>
    </template>

    <div class="space-y-2">
      <p class="text-sm">
        <span class="font-medium">Email:</span> {{ child.email }}
      </p>
      <p class="text-sm">
        <span class="font-medium">Баллы:</span> {{ child.points_balance }}
      </p>
      <div v-if="child.interests" class="text-sm">
        <span class="font-medium">Интересы:</span>
        <p class="text-gray-600">{{ child.interests }}</p>
      </div>
      <div v-if="child.preferences" class="text-sm">
        <span class="font-medium">Предпочтения:</span>
        <p class="text-gray-600">{{ child.preferences }}</p>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-2">
        <UButton
            variant="ghost"
            icon="i-heroicons-pencil"
            @click="$emit('edit')"
        >
          Изменить
        </UButton>
        <UButton
            variant="ghost"
            icon="i-heroicons-trash"
            color="red"
            @click="confirmDelete"
        >
          Удалить
        </UButton>
      </div>
    </template>
  </UCard>
</template>

<script setup>
const props = defineProps({
  child: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete'])

const confirmDelete = () => {
  // Можно добавить модальное окно подтверждения
  emit('delete')
}
</script>