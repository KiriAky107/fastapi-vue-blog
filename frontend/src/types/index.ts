// 用户相关类型
export interface User {
  id: string
  username: string
  email: string
  avatar?: string
  bio?: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface UserLoginRequest {
  email: string
  password: string
}

export interface UserRegisterRequest {
  username: string
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

// 文章相关类型
export interface Post {
  id: string
  title: string
  slug: string
  content: string
  summary?: string
  cover_image?: string
  author: User
  category?: Category
  tags: Tag[]
  view_count: number
  like_count?: number
  comment_count?: number
  status: 'draft' | 'published' | 'archived'
  meta_title?: string
  meta_description?: string
  published_at?: string
  created_at: string
  updated_at: string
}

export interface PostCreateRequest {
  title: string
  slug: string
  content: string
  summary?: string
  cover_image?: string
  category_id?: string
  tags?: string[]
  status?: 'draft' | 'published'
  meta_title?: string
  meta_description?: string
}

export interface PostUpdateRequest {
  title?: string
  slug?: string
  content?: string
  summary?: string
  cover_image?: string
  category_id?: string
  tags?: string[]
  status?: 'draft' | 'published' | 'archived'
  meta_title?: string
  meta_description?: string
}

export interface PostListResponse {
  items: Post[]
  total: number
  page: number
  page_size: number
  total_pages?: number
}

// 分类相关类型
export interface Category {
  id: string
  name: string
  slug: string
  description?: string
  created_at: string
}

// 标签相关类型
export interface Tag {
  id: string
  name: string
  slug?: string
  created_at: string
}

// 评论相关类型
export interface Comment {
  id: string
  content: string
  author?: User
  post_id?: string
  is_approved?: boolean
  created_at: string
  updated_at?: string
  parent_id?: string
  replies?: Comment[]
}

// API 响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页请求参数
export interface PageParams {
  page?: number
  page_size?: number
}
