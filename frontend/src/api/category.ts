import { http } from './index'
import type { Category } from '@/types'

export const categoryApi = {
  // 获取所有分类
  getAll() {
    return http.get<Category[]>('/categories')
  },

  // 获取单个分类
  getDetail(id: string) {
    return http.get<Category>(`/categories/${id}`)
  },
}
