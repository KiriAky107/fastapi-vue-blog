<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})

const phrases = ['探索二次元世界', '分享动漫资讯', '记录游戏攻略', '展现同人创作']
const currentPhrase = ref(0)

setInterval(() => {
  currentPhrase.value = (currentPhrase.value + 1) % phrases.length
}, 3000)
</script>

<template>
  <section class="hero">
    <!-- 背景动画 -->
    <div class="hero-bg">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <!-- 内容 -->
    <div class="hero-content" :class="{ visible: isVisible }">
      <!-- 标题 -->
      <h1 class="hero-title">ACG Blog</h1>

      <!-- 动态标语 -->
      <div class="phrase-container">
        <p class="phrase">{{ phrases[currentPhrase] }}<span class="cursor">|</span></p>
      </div>

      <!-- 描述 -->
      <p class="hero-desc">
        这里是二次元爱好者的聚集地，我们分享动漫、游戏、同人创作的点点滴滴。
      </p>

      <!-- 按钮组 -->
      <div class="hero-buttons">
        <RouterLink to="/" class="btn-primary">开始阅读</RouterLink>
        <RouterLink to="/about" class="btn-secondary">了解更多</RouterLink>
      </div>
    </div>

    <!-- 统计数字 -->
    <div class="stats" :class="{ visible: isVisible }">
      <div class="stat-item">
        <div class="stat-number">66+</div>
        <div class="stat-label">精彩文章</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">8+</div>
        <div class="stat-label">精选分类</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">42+</div>
        <div class="stat-label">热门标签</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">10k+</div>
        <div class="stat-label">访问量</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 6rem 1rem 3rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,231,246,0.3));
}
:global(.dark) .hero {
  background: linear-gradient(135deg, rgba(17,24,39,0.9), rgba(88,28,135,0.2));
}

.hero-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #FFB7C5, #FF69B4);
  top: -100px;
  left: -100px;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #A8D8EA, #87CEEB);
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #D4B5E6, #B57EDC);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(-30px, -20px) scale(1.02); }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease;
}
.hero-content.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6, #A8D8EA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
@media (min-width: 768px) {
  .hero-title {
    font-size: 4.5rem;
  }
}

.phrase-container {
  height: 2.5rem;
  margin-bottom: 1.5rem;
}

.phrase {
  font-size: 1.25rem;
  color: #6B7280;
}
:global(.dark) .phrase {
  color: #D1D5DB;
}

.cursor {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.hero-desc {
  max-width: 42rem;
  margin: 0 auto 2rem;
  font-size: 1rem;
  color: #9CA3AF;
  line-height: 1.75;
}

.hero-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.btn-primary {
  padding: 0.875rem 2rem;
  border-radius: 9999px;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  color: white;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(255, 183, 197, 0.4);
  transition: all 0.3s;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 183, 197, 0.6);
}

.btn-secondary {
  padding: 0.875rem 2rem;
  border-radius: 9999px;
  border: 2px solid #FFB7C5;
  color: #FFB7C5;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}
.btn-secondary:hover {
  background: #FFB7C5;
  color: white;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  max-width: 640px;
  margin-top: 3rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease 0.3s;
}
.stats.visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 0.25rem;
}
:global(.dark) .stat-label {
  color: #9CA3AF;
}
</style>
