export default defineNuxtConfig({
  compatibilityDate: '2025-01-20',
  modules: [
    '@nuxt/ui',
    '@nuxtjs/tailwindcss'
  ],
  css: [
    '@/assets/css/main.css'
  ],
  build: {
    transpile: ['@nuxt/ui']
  },
  devtools: {
    enabled: true
  },
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  app: {
    head: {
      title: 'KidTasks AI',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },
  ssr: false,
  devtools: { enabled: true },
  vite: {
    server: {
      watch: {
        usePolling: true,
        interval: 1000,
      },
      hmr: {
        protocol: 'ws',
        host: '0.0.0.0',
        port: 24678,
      }
    }
  },
  ui: {
    global: true,
    icons: ['heroicons'],
    primary: 'blue',
    gray: 'cool'
  },
  tailwindcss: {
    configPath: '~/tailwind.config.ts',
    exposeConfig: true,
    viewer: process.env.NODE_ENV === 'development'
  }
})
