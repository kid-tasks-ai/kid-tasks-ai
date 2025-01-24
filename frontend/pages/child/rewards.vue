<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Доступные награды</h1>

    <UCard>
      <template #header>
        <h2 class="text-lg font-medium">Магазин наград</h2>
      </template>

      <UAlert
          title="В разработке"
          description="Здесь будет отображаться список доступных наград"
          icon="i-heroicons-information-circle"
      />
    </UCard>
  </div>
</template>

<script>
export default {
  name: 'ChildRewardsPage',
  layout: 'child',
  middleware: ['child']
}
</script>