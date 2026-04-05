<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <div class="not-found min-h-screen">
    <Navbar />

    <!-- Hero Background -->
    <section class="relative py-16 px-4 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-blue-500/10"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-acg-pink/20 rounded-full blur-3xl"></div>
    </section>

    <!-- 404 Content -->
    <main class="px-4 pb-12 -mt-20 relative z-10 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-8xl font-bold text-acg-pink mb-4">404</h1>
        <p class="text-xl mb-6 text-gray-600 dark:text-gray-400">页面不存在</p>
        <RouterLink to="/" class="btn-acg inline-block">返回首页</RouterLink>
      </div>
    </main>

    <Footer />
  </div>
</template>
