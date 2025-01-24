<!-- components/rewards/RewardCard.vue -->
<template>
  <UCard :class="reward.is_redeemed ? 'bg-gray-50' : ''">
    <template #header>
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-medium">{{ reward.name }}</h3>
        <UBadge
            v-if="reward.is_redeemed"
            color="green"
            variant="solid"
        >
          Получено
        </UBadge>
      </div>
    </template>

    <div class="space-y-4">
      <p class="text-gray-600">{{ reward.description }}</p>

      <!-- Стоимость -->
      <div v-if="!reward.is_redeemed" class="space-y-2">
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium">
            {{ displayPoints }} / {{ reward.points_cost }} баллов
          </span>
          <span class="text-gray-500">{{ progressPercent }}%</span>
        </div>

        <UProgress
            :value="progressPercent"
            :color="hasEnoughPoints ? 'green' : 'blue'"
            :class="{ 'animate-pulse': hasEnoughPoints }"
        />
      </div>
      <div v-else class="text-sm">
        <span class="font-medium">{{ reward.points_cost }} баллов</span>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <UButton
            v-if="!reward.is_redeemed"
            :disabled="!hasEnoughPoints || loading"
            :loading="loading"
            color="primary"
            @click="$emit('redeem', reward.id)"
        >
          Получить награду
        </UButton>
        <div
            v-else
            class="text-sm text-gray-500"
        >
          Получено: {{ formatDate(reward.redeemed_at) }}
        </div>
      </div>
    </template>
  </UCard>
</template>

<script lang="ts">
import { type Reward } from '~/stores/childRewards'

export default {
  name: 'RewardCard',

  props: {
    reward: {
      type: Object as () => Reward,
      required: true
    },
    currentPoints: {
      type: Number,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },

  emits: ['redeem'],

  computed: {
    displayPoints(): number {
      return this.hasEnoughPoints ? this.reward.points_cost : this.currentPoints
    },

    progressPercent(): number {
      return Math.min(Math.round((this.currentPoints / this.reward.points_cost) * 100), 100)
    },

    hasEnoughPoints(): boolean {
      return this.currentPoints >= this.reward.points_cost
    }
  },

  methods: {
    formatDate(date: string | null): string {
      if (!date) return ''
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }).format(new Date(date))
    }
  }
}
</script>