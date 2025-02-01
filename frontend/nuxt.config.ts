// https://nuxt.com/docs/api/configuration/nuxt-config
import Theme from './assets/script/colors'

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['primeicons/primeicons.css', 'assets/css/main.css'],
  modules: [
    '@primevue/nuxt-module',
    "nuxt-phosphor-icons"
  ],
  primevue: {
    options: {
      theme: {
        preset: Theme,
        options: {
          prefix: 'p',
          darkModeSelector: '.dark-mode',
        }
      }
    }
  },
  server: {
    host: '127.0.0.1',
    port: 3001
  },
  devServer: {
    host: '127.0.0.1',
    port: 3001
  },
  app: {
    head: {
      meta: [
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
        }
      ],
      link: [
        {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
        {rel: 'apple-touch-icon', href: '/apple-icon-180x180.png'},
        {rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png'},
        {rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png'},
        {rel: 'manifest', href: '/site.webmanifest'}
      ]
    }
  }
})
