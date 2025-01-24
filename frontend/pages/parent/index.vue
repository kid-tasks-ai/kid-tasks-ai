<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6">Профиль родителя</h1>
    <div class="bg-white rounded-lg shadow p-6">
      <div class="mb-4">
        <h2 class="text-xl font-semibold">Личная информация</h2>
      </div>
      <div class="mt-4">
        <p class="text-gray-500">Раздел в разработке</p>
      </div>
    </div>
  </div>
</template>


<script>

definePageMeta({
  middleware: ['parent']
})

export default {
  name: 'ParentProfilePage',
  layout: 'parent',
}
</script>