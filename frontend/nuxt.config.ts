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
    enabled: process.env.NODE_ENV === 'development'
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
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Игровая платформа для развития детей через выполнение заданий' },
        { name: 'theme-color', content: '#ffffff' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'apple-mobile-web-app-title', content: 'KidTasks' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        // для modern browsers
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'manifest', href: '/manifest.json' },
        { rel: 'apple-touch-icon', href: '/icons/apple-touch-icon.png' }
      ]
    }
  },
  colorMode: {
    preference: 'light',
    fallback: 'light',
    classSuffix: '',
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE
    }
  },
  ssr: false,
  vite: {
    server: {
      watch: {
        usePolling: process.env.CHOKIDAR_USEPOLLING === 'true',
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
    exposeConfig: process.env.NODE_ENV === 'development',
    viewer: process.env.NODE_ENV === 'development'
  }
})