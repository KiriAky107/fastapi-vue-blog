import { http } from './index'
import type { Post, PostCreateRequest, PostUpdateRequest, PostListResponse, PageParams } from '@/types'

export const postApi = {
  // 获取文章列表
  getList(params?: PageParams & { category_id?: string; tag_id?: string }) {
    return http.get<PostListResponse>('/posts', { params })
  },

  // 获取单篇文章
  getDetail(id: string) {
    return http.get<Post>(`/posts/${id}`)
  },

  // 创建文章
  create(data: PostCreateRequest) {
    return http.post<Post>('/posts', data)
  },

  // 更新文章
  update(id: string, data: PostUpdateRequest) {
    return http.put<Post>(`/posts/${id}`, data)
  },

  // 删除文章
  delete(id: string) {
    return http.delete(`/posts/${id}`)
  },

  // 增加浏览量
  incrementView(id: string) {
    return http.post(`/posts/${id}/view`)
  },
}
