<script setup lang="ts">
import { RouterLink } from 'vue-router'

const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-grid">
        <!-- 博客信息 -->
        <div class="footer-section footer-about">
          <div class="footer-logo">
            <div class="logo-icon">A</div>
            <span class="logo-text">ACG Blog</span>
          </div>
          <p class="footer-desc">
            专注于二次元文化的博客平台，分享动漫、游戏、同人创作等内容。
          </p>
          <div class="social-links">
            <a href="#" class="social-link" title="GitHub">GH</a>
            <a href="#" class="social-link" title="Twitter">X</a>
            <a href="#" class="social-link" title="Telegram">TG</a>
          </div>
        </div>

        <!-- 快速链接 -->
        <div class="footer-section">
          <h4 class="footer-title">快速链接</h4>
          <ul class="footer-links">
            <li><RouterLink to="/">首页</RouterLink></li>
            <li><RouterLink to="/about">关于</RouterLink></li>
            <li><RouterLink to="/archive">归档</RouterLink></li>
            <li><RouterLink to="/login">登录</RouterLink></li>
          </ul>
        </div>

        <!-- 合作伙伴 -->
        <div class="footer-section">
          <h4 class="footer-title">合作伙伴</h4>
          <ul class="footer-links">
            <li><a href="#">B站</a></li>
            <li><a href="#">NGA</a></li>
            <li><a href="#">AcFun</a></li>
          </ul>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="footer-bottom">
        <p>© {{ currentYear }} ACG Blog. All rights reserved.</p>
        <div class="footer-legal">
          <a href="#">隐私政策</a>
          <a href="#">服务条款</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: linear-gradient(to bottom, transparent, rgba(249, 250, 251, 0.5));
  margin-top: 4rem;
}
:global(.dark) .footer {
  background: linear-gradient(to bottom, transparent, rgba(17, 24, 39, 0.5));
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 3rem 1rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}
@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: 2fr 1fr 1fr;
  }
}

.footer-section {
  min-width: 0;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.logo-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.25rem;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: bold;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-desc {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 1rem;
}
:global(.dark) .footer-desc {
  color: #9CA3AF;
}

.social-links {
  display: flex;
  gap: 0.75rem;
}

.social-link {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 9999px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  text-decoration: none;
  transition: all 0.2s;
}
:global(.dark) .social-link {
  background: #374151;
  color: #9CA3AF;
}
.social-link:hover {
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  color: white;
  transform: translateY(-2px);
}

.footer-title {
  font-weight: 600;
  margin-bottom: 1rem;
  color: #FFB7C5;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.5rem;
}

.footer-links a {
  color: #6B7280;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}
:global(.dark) .footer-links a {
  color: #9CA3AF;
}
.footer-links a:hover {
  color: #FFB7C5;
}

.footer-bottom {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}
:global(.dark) .footer-bottom {
  border-top-color: #374151;
}
@media (min-width: 768px) {
  .footer-bottom {
    flex-direction: row;
    justify-content: space-between;
  }
}

.footer-bottom p {
  font-size: 0.875rem;
  color: #9CA3AF;
}

.footer-legal {
  display: flex;
  gap: 1rem;
}

.footer-legal a {
  font-size: 0.875rem;
  color: #9CA3AF;
  text-decoration: none;
  transition: color 0.2s;
}
.footer-legal a:hover {
  color: #FFB7C5;
}
</style>
