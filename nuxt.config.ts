// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxtjs/supabase', '@nuxt/ui'],
  css: ['@/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  supabase: {
    redirect: false,
    redirectOptions: {
      login: '/auth/login',
      callback: '/auth/callback',
    },
  },
})