import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 在发送请求之前做些什么
    // 例如添加token
    const token = localStorage.getItem('token') || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc5ODFiMDdmLTAzZjMtNGY1MC04ODA4LWNlYTVlNmRlOGUzNiIsImxvZ2luX2luZm8iOm51bGwsImV4cCI6MjAxOTczNzU3N30.Gc3JPHkw3MmLvqd6meRRusCoN7l_l-dOnB5djNE3EG0'
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // 对请求错误做些什么
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    const { code, message, data } = response.data

    if (code === 200) {
      return response.data
    } else {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message || '请求失败'))
    }
  },
  (error) => {
    // 对响应错误做点什么
    console.error('Response error:', error)

    if (error.response?.status === 401) {
      // 处理未授权
      ElMessage.error('登录已过期，请重新登录')
      // 可以在这里处理登出逻辑
    } else {
      ElMessage.error(error.message || '网络错误')
    }

    return Promise.reject(error)
  }
)

export default service


function instancePromise<R = any, T = any>(options: AxiosOptions<T> & RequestConfigExtra): Promise<ResponseBody<R>> {
    const {loading} = options
    return new Promise((resolve, reject) => {
        service.request(options).then((res: any) => {
            resolve(res as any)
        }).catch((e: Error | AxiosError) => {
            reject(e)
        })
            .finally(() => {
                if (loading)
                    axiosLoading.closeLoading()
            })
    })
}

export function useGet<R = any, T = any>(url: string, params?: T, config?: AxiosRequestConfig & RequestConfigExtra): Promise<ResponseBody<R>> {
    const options = {
        url,
        params,
        method: "GET",
        ...config,
    }
    return instancePromise<R, T>(options)
}

export function useGetBlob<R = any, T = any>(url: string, params?: T, config?: AxiosRequestConfig & RequestConfigExtra): Promise<ResponseBody<R>> {
    const options = {
        url,
        params,
        responseType: 'blob',
        method: "GET",
        ...config,
    }
    return instancePromise<R, T>(options)
}

export function usePost<R = any, T = any>(url: string, data?: T, config?: AxiosRequestConfig & RequestConfigExtra): Promise<ResponseBody<R>> {
    const options = {
        url,
        data,
        method: "POST",
        ...config,
    }
    return instancePromise<R, T>(options)
}

export function usePut<R = any, T = any>(url: string, data?: T, config?: AxiosRequestConfig & RequestConfigExtra): Promise<ResponseBody<R>> {
    const options = {
        url,
        data,
        method: "PUT",
        ...config,
    }
    return instancePromise<R, T>(options)
}

export function useDelete<R = any, T = any>(url: string, data?: T, config?: AxiosRequestConfig & RequestConfigExtra): Promise<ResponseBody<R>> {
    const options = {
        url,
        data,
        method: "DELETE",
        ...config,
    }
    return instancePromise<R, T>(options)
}
