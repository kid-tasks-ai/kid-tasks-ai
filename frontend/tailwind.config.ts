import type { Config } from 'tailwindcss'
import defaultTheme from 'tailwindcss/defaultTheme'

export default <Config>{
  theme: {
    extend: {
      colors: {
        // Добавляем цвета из defaultTheme
        ...defaultTheme.colors
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
    './error.vue',
  ]
}