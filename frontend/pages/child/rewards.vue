<!-- pages/child/rewards.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Доступные награды</h1>

    <!-- Фильтры -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex gap-4 items-center">
        <USelect
            v-model="filter"
            :options="[
              { label: 'Все награды', value: null },
              { label: 'Доступные', value: 'available' },
              { label: 'Полученные', value: 'redeemed' }
            ]"
            option-attribute="label"
            value-attribute="value"
            class="w-48"
        />
      </div>
    </div>

    <!-- Список наград -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress />
    </div>

    <UAlert
        v-else-if="error"
        :title="error"
        color="red"
        variant="soft"
        class="mb-4"
    />

    <div v-else-if="displayedRewards.length === 0" class="text-center py-8">
      <UIcon
          name="i-heroicons-gift"
          class="mx-auto h-12 w-12 text-gray-400"
      />
      <h3 class="mt-2 text-sm font-semibold text-gray-900">
        {{ getEmptyStateText }}
      </h3>
      <p class="mt-1 text-sm text-gray-500">
        {{ getEmptyStateDescription }}
      </p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <RewardCard
          v-for="reward in displayedRewards"
          :key="reward.id"
          :reward="reward"
          :current-points="pointsBalance"
          :loading="redeemingId === reward.id"
          @redeem="handleRedeem"
      />
    </div>
  </div>
</template>

<script>
import { useChildRewardsStore } from '~/stores/childRewards'
import { useChildProfileStore } from '~/stores/childProfile'
import RewardCard from '~/components/rewards/RewardCard.vue'

definePageMeta({
  middleware: ['child']
})

export default {
  name: 'ChildRewardsPage',
  layout: 'child',
  components: { RewardCard },

  data() {
    return {
      filter: null,
      redeemingId: null,
      loading: false,
      error: null,
      rewardsStore: null,
      profileStore: null
    }
  },

  computed: {
    pointsBalance() {
      return this.profileStore?.pointsBalance || 0
    },

    displayedRewards() {
      const rewards = this.rewardsStore?.rewards || []

      if (this.filter === 'available') {
        return rewards.filter(reward => !reward.is_redeemed)
      }
      if (this.filter === 'redeemed') {
        return rewards.filter(reward => reward.is_redeemed)
      }

      return rewards
    },

    getEmptyStateText() {
      if (this.filter === 'available') {
        return 'Нет доступных наград'
      }
      if (this.filter === 'redeemed') {
        return 'Нет полученных наград'
      }
      return 'Нет наград'
    },

    getEmptyStateDescription() {
      if (this.filter === 'available') {
        return 'Зарабатывайте баллы, выполняя задания!'
      }
      if (this.filter === 'redeemed') {
        return 'Выполняйте задания и получайте награды!'
      }
      return 'Скоро здесь появятся награды'
    }
  },

  watch: {
    filter() {
      this.loadRewards()
    }
  },

  created() {
    this.rewardsStore = useChildRewardsStore()
    this.profileStore = useChildProfileStore()
    this.loadRewards()
  },

  methods: {
    async loadRewards() {
      this.loading = true
      this.error = null

      try {
        let isRedeemed
        if (this.filter === 'available') {
          isRedeemed = false
        } else if (this.filter === 'redeemed') {
          isRedeemed = true
        }

        await this.rewardsStore.fetchRewards({ is_redeemed: isRedeemed })
      } catch (err) {
        console.error('Error loading rewards:', err)
        this.error = 'Не удалось загрузить список наград'
      } finally {
        this.loading = false
      }
    },

    async handleRedeem(rewardId) {
      this.redeemingId = rewardId

      try {
        await this.rewardsStore.redeemReward(rewardId)
        // Обновляем профиль для получения актуального баланса
        await this.profileStore.fetchProfile()
      } catch (err) {
        console.error('Error redeeming reward:', err)
        // TODO: Показать уведомление об ошибке
      } finally {
        this.redeemingId = null
      }
    }
  }
}
</script>