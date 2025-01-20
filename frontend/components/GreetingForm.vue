<template>
  <div class="max-w-md">
    <div class="mb-4">
      <input
        v-model="name"
        type="text"
        placeholder="Введите ваше имя"
        class="w-full px-4 py-2 border rounded-lg"
      />
    </div>
    <button
      @click="greet"
      class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
    >
      Поприветствовать
    </button>
    <div v-if="greeting" class="mt-4 text-lg">
      {{ greeting }}
    </div>
  </div>
</template>

<script setup>
const name = ref('')
const greeting = ref('')

const greet = () => {
  if (name.value) {
    greeting.value = `Привет, ${name.value}!`
  }
}
</script>