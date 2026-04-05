<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="admin-layout min-h-screen">
    <!-- Admin Navbar -->
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center gap-4">
          <div class="text-xl font-bold bg-gradient-to-r from-acg-pink to-acg-purple bg-clip-text text-transparent">
            ACG Blog
          </div>
          <span class="text-gray-400">|</span>
          <span class="text-sm text-gray-500">管理后台</span>
        </div>
        <RouterLink to="/" class="text-sm hover:text-acg-pink transition-colors">
          返回前台
        </RouterLink>
      </div>
    </nav>

    <!-- Admin Content -->
    <main class="pt-24 px-4 pb-12 max-w-6xl mx-auto">
      <div class="flex gap-6">
        <!-- 侧边栏 -->
        <aside class="w-48 flex-shrink-0">
          <nav class="glass rounded-xl p-4 space-y-2">
            <RouterLink
              to="/admin/dashboard"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors text-gray-700 dark:text-gray-300"
              active-class="bg-acg-pink/20 text-acg-pink"
            >
              📊 仪表盘
            </RouterLink>
            <RouterLink
              to="/admin/posts"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors text-gray-700 dark:text-gray-300"
              active-class="bg-acg-pink/20 text-acg-pink"
            >
              📝 文章管理
            </RouterLink>
            <RouterLink
              to="/admin/categories"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors text-gray-700 dark:text-gray-300"
              active-class="bg-acg-pink/20 text-acg-pink"
            >
              📁 分类管理
            </RouterLink>
            <RouterLink
              to="/admin/tags"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors text-gray-700 dark:text-gray-300"
              active-class="bg-acg-pink/20 text-acg-pink"
            >
              🏷️ 标签管理
            </RouterLink>
          </nav>
        </aside>

        <!-- 主内容区 -->
        <main class="flex-1">
          <RouterView />
        </main>
      </div>
    </main>

    <!-- Admin Footer -->
    <footer class="py-6 text-center text-sm text-gray-500">
      <p>© {{ new Date().getFullYear() }} ACG Blog Admin. All rights reserved.</p>
    </footer>
  </div>
</template>
