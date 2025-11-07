// 通用响应接口
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 用户接口
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  createdAt: string
  updatedAt: string
}

// 分页接口
export interface Pagination {
  page: number
  pageSize: number
  total: number
}

// 列表响应接口
export interface ListResponse<T> {
  list: T[]
  pagination: Pagination
}