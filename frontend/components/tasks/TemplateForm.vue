<!-- components/tasks/TemplateForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <UFormGroup label="Название задания" required>
      <UInput
          v-model="form.title"
          placeholder="Введите название задания"
          :error="errors.title"
          required
      />
    </UFormGroup>

    <UFormGroup label="Описание" required>
      <UTextarea
          v-model="form.description"
          placeholder="Опишите задание"
          :error="errors.description"
          rows="3"
          required
      />
    </UFormGroup>

    <UFormGroup label="Баллы за выполнение" required>
      <UInput
          v-model="form.points_value"
          type="number"
          min="1"
          placeholder="Укажите количество баллов"
          :error="errors.points_value"
          required
      />
    </UFormGroup>

    <UFormGroup label="Тип расписания" required>
      <USelect
          v-model="form.schedule_type"
          :options="scheduleTypes"
          option-attribute="label"
          value-attribute="value"
          :error="errors.schedule_type"
          required
      />
    </UFormGroup>

    <!-- Дополнительные настройки для еженедельного расписания -->
    <UFormGroup v-if="form.schedule_type === 'weekly'" label="Дни недели">
      <div class="flex flex-wrap gap-2">
        <UButton
            v-for="day in weekDays"
            :key="day.value"
            :variant="isWeekDaySelected(day.value) ? 'solid' : 'outline'"
            color="primary"
            @click="toggleWeekDay(day.value)"
            type="button"
        >
          {{ day.label }}
        </UButton>
      </div>
      <span v-if="errors.schedule_settings" class="text-sm text-red-500">
        {{ errors.schedule_settings }}
      </span>
    </UFormGroup>

    <UFormGroup>
      <UToggle v-model="form.is_active">
        <span class="ml-2">Шаблон активен</span>
      </UToggle>
    </UFormGroup>

    <div class="flex justify-end gap-2 mt-6">
      <UButton
          type="button"
          variant="ghost"
          @click="$emit('cancel')"
      >
        Отмена
      </UButton>
      <UButton
          type="submit"
          color="primary"
          :loading="loading"
      >
        {{ submitButtonText }}
      </UButton>
    </div>
  </form>
</template>

<script>
export default {
  name: 'TemplateForm',

  props: {
    initialData: {
      type: Object,
      default: () => ({})
    },
    childId: {
      type: Number,
      required: true
    },
    loading: {
      type: Boolean,
      required: true
    }
  },

  emits: ['submit', 'cancel'],

  data() {
    return {
      form: {
        title: '',
        description: '',

        points_value: 1,
        schedule_type: 'once',
        schedule_settings: {},
        is_active: true,
        child_id: this.childId
      },
      errors: {},

      scheduleTypes: [
        { label: 'Единоразово', value: 'once' },
        { label: 'Ежедневно', value: 'daily' },
        { label: 'Еженедельно', value: 'weekly' }
      ],
      weekDays: [
        { label: 'Пн', value: 1 },
        { label: 'Вт', value: 2 },
        { label: 'Ср', value: 3 },
        { label: 'Чт', value: 4 },
        { label: 'Пт', value: 5 },
        { label: 'Сб', value: 6 },
        { label: 'Вс', value: 0 }
      ]
    }
  },

  computed: {
    submitButtonText() {
      return this.initialData?.id ? 'Сохранить' : 'Создать'
    }
  },

  watch: {
    initialData: {
      handler(newData) {
        if (newData?.id) {
          this.initForm(newData)
        }
      },
      immediate: true
    },
    'form.schedule_type'(newType) {
      if (newType !== 'weekly') {
        this.form.schedule_settings = {}
      } else if (!this.form.schedule_settings?.weekDays) {
        this.form.schedule_settings = { weekDays: [] }
      }
    }
  },

  methods: {
    initForm(data) {
      this.form = {
        title: data.title || '',
        description: data.description || '',

        points_value: data.points_value || 1,
        schedule_type: data.schedule_type || 'once',
        schedule_settings: data.schedule_settings || {},
        is_active: data.is_active !== undefined ? data.is_active : true,
        child_id: this.childId
      }
      this.errors = {}
    },

    isWeekDaySelected(day) {
      return this.form.schedule_settings?.weekDays?.includes(day)
    },

    toggleWeekDay(day) {
      if (!this.form.schedule_settings.weekDays) {
        this.form.schedule_settings.weekDays = []
      }

      const index = this.form.schedule_settings.weekDays.indexOf(day)
      if (index === -1) {
        this.form.schedule_settings.weekDays.push(day)
      } else {
        this.form.schedule_settings.weekDays.splice(index, 1)
      }
    },

    validate() {
      this.errors = {}

      if (!this.form.title?.trim()) {
        this.errors.title = 'Укажите название задания'
      }

      if (!this.form.description?.trim()) {
        this.errors.description = 'Добавьте описание задания'
      }

      if (!this.form.points_value || this.form.points_value < 1) {
        this.errors.points_value = 'Укажите количество баллов (минимум 1)'
      }

      if (this.form.schedule_type === 'weekly' &&
          (!this.form.schedule_settings?.weekDays?.length)) {
        this.errors.schedule_settings = 'Выберите хотя бы один день недели'
      }

      return Object.keys(this.errors).length === 0
    },

    handleSubmit() {
      if (this.validate()) {
        this.$emit('submit', { ...this.form })
      }
    }
  }
}
</script>