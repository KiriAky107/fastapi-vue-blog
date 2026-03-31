import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'

// 创建 axios 实例
const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config: any) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: any) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 成功时返回 response.data（即 ApiResponse）
    return response.data
  },
  (error: any) => {
    if (error.response) {
      const { status, data } = error.response

      // 401 未授权，清除 token
      if (status === 401) {
        localStorage.removeItem('access_token')
        window.location.href = '/login'
      }

      // 返回错误信息
      return Promise.reject(data)
    }

    return Promise.reject(error)
  }
)

// 封装请求方法
// 返回 Promise<ApiResponse<T>>，调用者通过 .data 访问实际数据
export const http = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<{ code: number; message: string; data: T }> {
    return request.get(url, config).then(res => res.data)
  },

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<{ code: number; message: string; data: T }> {
    return request.post(url, data, config).then(res => res.data)
  },

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<{ code: number; message: string; data: T }> {
    return request.put(url, data, config).then(res => res.data)
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<{ code: number; message: string; data: T }> {
    return request.delete(url, config).then(res => res.data)
  },
}

export default request
