import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('@/views/PostDetail.vue'),
  },
  {
    path: '/category/:id',
    name: 'Category',
    component: () => import('@/views/Category.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
  },
  {
    path: '/archive',
    name: 'Archive',
    component: () => import('@/views/Archive.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/user/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard',
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
      },
      {
        path: 'posts',
        name: 'AdminPosts',
        component: () => import('@/views/admin/PostManage.vue'),
      },
      {
        path: 'categories',
        name: 'AdminCategories',
        component: () => import('@/views/admin/CategoryManage.vue'),
      },
      {
        path: 'tags',
        name: 'AdminTags',
        component: () => import('@/views/admin/TagManage.vue'),
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore()
  const token = localStorage.getItem('access_token')

  // 需要登录但未登录
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
    return
  }

  // 需要管理员权限但不是管理员
  if (to.meta.requiresAdmin) {
    // 如果还没有用户信息，先获取
    if (!userStore.user && token) {
      try {
        await userStore.fetchUser()
      } catch {
        // 获取失败，清除 token
        userStore.logout()
        next({ name: 'Login' })
        return
      }
    }

    if (!userStore.user?.is_superuser) {
      next({ name: 'Home' })
      return
    }
  }

  next()
})

export default router
