<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Профиль родителя</h1>
    <div class="bg-white rounded-lg shadow p-6">
      <div class="mb-4">
        <h2 class="text-xl font-semibold">Личная информация</h2>
      </div>
      <div class="mt-4">
        <!-- Здесь будет форма профиля -->
        <p class="text-gray-500">Раздел в разработке</p>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'parent',
  middleware: ['parent']
})
</script>