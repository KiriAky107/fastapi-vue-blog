<template>
  <div class="admin-layout min-h-screen">
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="text-xl font-bold text-acg-pink">管理后台</div>
        <RouterLink to="/" class="text-sm hover:text-acg-pink">返回前台</RouterLink>
      </div>
    </nav>

    <div class="pt-20 px-4 max-w-6xl mx-auto">
      <div class="flex gap-6">
        <!-- 侧边栏 -->
        <aside class="w-48 flex-shrink-0">
          <nav class="glass rounded-xl p-4 space-y-2">
            <RouterLink
              to="/admin/dashboard"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors"
            >
              仪表盘
            </RouterLink>
            <RouterLink
              to="/admin/posts"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors"
            >
              文章管理
            </RouterLink>
            <RouterLink
              to="/admin/categories"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors"
            >
              分类管理
            </RouterLink>
            <RouterLink
              to="/admin/tags"
              class="block px-4 py-2 rounded-lg hover:bg-acg-pink/10 transition-colors"
            >
              标签管理
            </RouterLink>
          </nav>
        </aside>

        <!-- 主内容区 -->
        <main class="flex-1">
          <RouterView />
        </main>
      </div>
    </div>
  </div>
</template>
