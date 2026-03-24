import { http } from './index'
import type { UserLoginRequest, UserRegisterRequest, TokenResponse, User } from '@/types'

export const authApi = {
  // 用户登录
  login(data: UserLoginRequest) {
    return http.post<TokenResponse>('/auth/login', data)
  },

  // 用户注册
  register(data: UserRegisterRequest) {
    return http.post<User>('/auth/register', data)
  },

  // 获取当前用户信息
  getCurrentUser() {
    return http.get<User>('/auth/me')
  },

  // 刷新 Token
  refreshToken(refreshToken: string) {
    return http.post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken })
  },

  // 登出
  logout() {
    return http.post('/auth/logout')
  },
}
