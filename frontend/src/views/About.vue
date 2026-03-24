<template>
  <div class="about">
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <RouterLink to="/" class="text-acg-pink hover:underline">← 返回首页</RouterLink>
      </div>
    </nav>

    <main class="pt-20 px-4 max-w-4xl mx-auto">
      <div class="glass rounded-xl p-8">
        <h1 class="text-3xl font-bold mb-4">关于 ACG Blog</h1>
        <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
          ACG Blog 是一个专注于二次元文化的博客平台，使用 Vue 3 + TypeScript + Naive UI 构建。
          在这里，你可以分享你的二次元生活、动漫评论、游戏攻略等内容。
        </p>
      </div>
    </main>
  </div>
</template>
