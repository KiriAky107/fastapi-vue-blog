<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

async function handleLogin() {
  // TODO: 实现登录逻辑
  console.log('Login:', email.value, password.value)
  router.push('/')
}
</script>

<template>
  <div class="login min-h-screen flex items-center justify-center px-4">
    <div class="glass rounded-xl p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">登录</h1>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            placeholder="请输入邮箱"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-acg-pink"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-acg-pink"
            required
          />
        </div>

        <button type="submit" class="w-full btn-acg">
          登录
        </button>
      </form>

      <p class="text-center mt-4 text-sm">
        还没有账号？
        <RouterLink to="/register" class="text-acg-pink hover:underline">立即注册</RouterLink>
      </p>
    </div>
  </div>
</template>
