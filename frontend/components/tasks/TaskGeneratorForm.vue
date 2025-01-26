<template>
  <UModal
      :model-value="isOpen"
      @close="$emit('close')"
  >
    <div class="p-4">
      <h2 class="text-lg font-medium mb-4">Генерация заданий</h2>

      <UForm :state="form" @submit="handleSubmit" class="space-y-4">
        <UFormGroup label="Пожелания к заданиям">
          <UTextarea
              v-model="form.description"
              placeholder="Опишите, какие задания вы хотели бы сгенерировать"
              required
          />
        </UFormGroup>

        <UFormGroup label="Количество заданий">
          <UInput
              v-model="form.count"
              type="number"
              :rules="{ required: true, min: 1, max: 10 }"
          />
        </UFormGroup>

        <div class="flex justify-end gap-2 mt-6">
          <UButton
              variant="ghost"
              @click="$emit('close')"
          >
            Отмена
          </UButton>
          <UButton
              type="submit"
              :loading="loading"
              color="purple"
              icon="i-heroicons-sparkles"
              class="relative group"
          >
            <div class="flex items-center gap-2">
              <span>Сгенерировать</span>
              <div class="absolute inset-0 rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-0 group-hover:opacity-20 transition-opacity"></div>
            </div>
          </UButton>
        </div>
      </UForm>
    </div>
  </UModal>
</template>

<script>
import { useTemplatesStore } from '~/stores/templates'

export default {
  name: 'TaskGenerator',

  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    childId: {
      type: Number,
      required: true
    }
  },

  emits: ['close', 'success'],

  setup() {
    const templatesStore = useTemplatesStore()
    return { templatesStore }
  },

  data() {
    return {
      loading: false,
      form: {
        description: '',
        count: 3
      }
    }
  },

  methods: {
    async handleSubmit() {
      this.loading = true
      try {
        const response = await this.templatesStore.generateTasks({
          child_id: this.childId,
          task_count: this.form.count,
          description: this.form.description
        })

        if (response.status === 'success') {
          const { $notify } = useNuxtApp()
          $notify.success('Задания успешно сгенерированы')
          this.$emit('success')
          this.$emit('close')
        }
      } catch (error) {
        const { $notify } = useNuxtApp()
        $notify.error(error.data?.detail || 'Ошибка при генерации заданий')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>