<script setup lang="ts">
import { useThemeStore } from '@/store/theme'
import { useUserStore } from '@/store/user'
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const themeStore = useThemeStore()
const userStore = useUserStore()
const route = useRoute()

const isAdmin = computed(() => route.path.startsWith('/admin'))
</script>

<template>
  <nav v-if="!isAdmin" class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <div class="logo-icon">A</div>
        <span class="logo-text">ACG Blog</span>
      </RouterLink>

      <!-- 导航链接 -->
      <div class="nav-links">
        <RouterLink to="/" class="nav-link" exact-active-class="active">首页</RouterLink>
        <RouterLink to="/category" class="nav-link" active-class="active">分类</RouterLink>
        <RouterLink to="/archive" class="nav-link" active-class="active">归档</RouterLink>
        <RouterLink to="/about" class="nav-link" active-class="active">关于</RouterLink>
      </div>

      <!-- 右侧操作区 -->
      <div class="nav-actions">
        <!-- 主题切换 -->
        <button @click="themeStore.toggleTheme()" class="action-btn" :title="themeStore.theme === 'light' ? '切换深色模式' : '切换浅色模式'">
          <span class="text-lg">{{ themeStore.theme === 'light' ? '🌙' : '☀️' }}</span>
        </button>

        <!-- 登录按钮 -->
        <RouterLink v-if="!userStore.isLoggedIn" to="/login" class="login-btn">
          登录
        </RouterLink>
        <RouterLink v-else to="/profile" class="user-avatar" :title="userStore.user?.username">
          {{ userStore.user?.username?.[0]?.toUpperCase() || 'U' }}
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.3);
}
:global(.dark) .navbar {
  background: rgba(17, 24, 39, 0.8);
  border-bottom-color: rgba(75, 85, 99, 0.3);
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.logo-icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.625rem;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.125rem;
  box-shadow: 0 2px 10px rgba(255, 183, 197, 0.3);
}

.logo-text {
  font-size: 1.25rem;
  font-weight: bold;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: none;
  gap: 0.5rem;
}
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  position: relative;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s;
}
:global(.dark) .nav-link {
  color: #9CA3AF;
}
.nav-link:hover {
  color: #FFB7C5;
  background: rgba(255, 183, 197, 0.1);
}
.nav-link.active {
  color: #FFB7C5;
  background: rgba(255, 183, 197, 0.15);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.action-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
:global(.dark) .action-btn {
  background: #374151;
}
.action-btn:hover {
  background: rgba(255, 183, 197, 0.3);
  transform: scale(1.05);
}

.login-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 2px 10px rgba(255, 183, 197, 0.3);
}
.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(255, 183, 197, 0.5);
}

.user-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 2px 10px rgba(255, 183, 197, 0.3);
  transition: all 0.2s;
}
.user-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(255, 183, 197, 0.5);
}
</style>
