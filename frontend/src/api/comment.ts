import { http } from './index'
import type { Comment, ApiResponse, PageParams } from '@/types'

export interface CommentCreateRequest {
  post_id: string
  content: string
  parent_id?: string
}

export interface CommentUpdateRequest {
  content: string
}

export interface CommentListResponse {
  items: Comment[]
  total: number
  page: number
  page_size: number
}

export const commentApi = {
  /**
   * 获取文章的评论列表
   */
  getByPost(postId: string, params?: PageParams & { approved_only?: boolean }): Promise<ApiResponse<CommentListResponse>> {
    return http.get<CommentListResponse>(`/comments/post/${postId}`, { params })
  },

  /**
   * 创建评论
   */
  create(data: CommentCreateRequest): Promise<ApiResponse<Comment>> {
    return http.post<Comment>('/comments', data)
  },

  /**
   * 更新评论
   */
  update(commentId: string, data: CommentUpdateRequest): Promise<ApiResponse<Comment>> {
    return http.put<Comment>(`/comments/${commentId}`, data)
  },

  /**
   * 删除评论
   */
  delete(commentId: string): Promise<ApiResponse<void>> {
    return http.delete(`/comments/${commentId}`)
  },
}
