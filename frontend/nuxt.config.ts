export default defineNuxtConfig({
  compatibilityDate: '2025-01-20',
  modules: ['@nuxtjs/tailwindcss'],
  app: {
    head: {
      title: 'KidTasks AI',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  }
})