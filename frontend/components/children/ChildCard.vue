<!-- components/children/ChildCard.vue -->
<template>
  <UCard>
    <template #header>
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2">
          <UIcon
              name="i-heroicons-user-circle"
              class="w-5 h-5"
              :class="genderIconColor"
          />
          <h3 class="text-lg font-medium">{{ child.name }}</h3>
        </div>
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

<script>
export default {
  name: 'ChildCard',

  props: {
    child: {
      type: Object,
      required: true,
      validator(child) {
        return (
            'name' in child &&
            'age' in child &&
            'email' in child &&
            'points_balance' in child
        )
      }
    }
  },

  emits: ['edit', 'delete'],
  computed: {
    genderIconColor() {
      return this.child.gender === 'male' ? 'text-blue-500' : 'text-pink-500'
    }
  },
  methods: {
    confirmDelete() {
      this.$emit('delete')
    }
  }
}
</script>
