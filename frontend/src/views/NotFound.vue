<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="not-found min-h-screen flex items-center justify-center px-4">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-acg-pink mb-4">404</h1>
      <p class="text-xl mb-6">页面不存在</p>
      <RouterLink to="/" class="btn-acg">返回首页</RouterLink>
    </div>
  </div>
</template>
