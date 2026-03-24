<script setup lang="ts">
import { useThemeStore } from '@/store/theme'
import { useUserStore } from '@/store/user'
import { RouterLink } from 'vue-router'

const themeStore = useThemeStore()
const userStore = useUserStore()
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <div class="logo-icon">A</div>
        <span class="logo-text">ACG Blog</span>
      </RouterLink>

      <!-- 导航链接 -->
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">首页</RouterLink>
        <RouterLink to="/category" class="nav-link">分类</RouterLink>
        <RouterLink to="/archive" class="nav-link">归档</RouterLink>
        <RouterLink to="/about" class="nav-link">关于</RouterLink>
      </div>

      <!-- 右侧操作区 -->
      <div class="nav-actions">
        <!-- 主题切换 -->
        <button @click="themeStore.toggleTheme()" class="action-btn">
          {{ themeStore.theme === 'light' ? '☀️' : themeStore.theme === 'dark' ? '🌙' : '🌗' }}
        </button>

        <!-- 登录按钮 -->
        <RouterLink v-if="!userStore.isLoggedIn" to="/login" class="login-btn">
          登录
        </RouterLink>
        <RouterLink v-else to="/profile" class="user-avatar">
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
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
}
:global(.dark) .navbar {
  background: rgba(17, 24, 39, 0.85);
  border-bottom-color: rgba(75, 85, 99, 0.5);
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
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
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.125rem;
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
  gap: 1.5rem;
}
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  position: relative;
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s;
}
:global(.dark) .nav-link {
  color: #9CA3AF;
}
.nav-link:hover,
.nav-link.router-link-active {
  color: #FFB7C5;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.action-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 9999px;
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
  background: #FFB7C5;
}

.login-btn {
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  border: 2px solid #FFB7C5;
  color: #FFB7C5;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}
.login-btn:hover {
  background: #FFB7C5;
  color: white;
}

.user-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 9999px;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  text-decoration: none;
}
</style>
