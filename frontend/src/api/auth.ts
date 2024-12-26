import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('=== 发送请求 ===')
    console.log('请求URL:', config.url)
    console.log('请求方法:', config.method)
    
    // 确保 headers 对象存在
    config.headers = config.headers || {}
    
    const token = localStorage.getItem('token')
    if (token) {
      // 确保 token 格式正确
      config.headers.Authorization = `Bearer ${token}`
      console.log('添加认证头:', config.headers.Authorization)
    } else {
      console.log('No token found')
    }
    
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('=== 收到响应 ===')
    console.log('响应状态:', response.status)
    console.log('响应数据:', response.data)
    return response.data
  },
  (error) => {
    console.error('=== 响应错误 ===')
    console.error('错误信息:', error.message)
    
    const err = {
      status: error.response?.status,
      message: error.response?.data?.message || error.response?.data?.msg || '请求失败',
      data: error.response?.data
    }
    
    if (error.response) {
      console.error('响应状态:', error.response.status)
      console.error('响应数据:', error.response.data)
    }
    
    return Promise.reject(err)
  }
)

export interface LoginData {
  username: string
  password: string
}

export interface ChangePasswordData {
  old_password: string
  new_password: string
}

export interface UserInfo {
  id: number
  username: string
  email: string | null
  created_at: string
  updated_at: string
}

export interface LoginResponse {
  access_token: string
  user: UserInfo
}

export const authApi = {
  login: async (data: LoginData): Promise<LoginResponse> => {
    console.log('=== 开始登录请求 ===')
    console.log('登录数据:', data)
    try {
      const response = await api.post<any, LoginResponse>('/auth/login', data)
      console.log('登录成功:', response)
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  },
    
  changePassword: async (data: ChangePasswordData): Promise<{ message: string }> => {
    console.log('=== 开始修改密码请求 ===')
    try {
      const response = await api.post<any, { message: string }>('/auth/change-password', data)
      console.log('修改密码成功:', response)
      return response
    } catch (error) {
      console.error('修改密码失败:', error)
      throw error
    }
  },
    
  getProfile: async (): Promise<UserInfo> => {
    console.log('=== 开始获取用户信息请求 ===')
    const token = localStorage.getItem('token')
    console.log('当前 token:', token)
    
    if (!token) {
      throw new Error('未登录')
    }
    
    try {
      const response = await api.get<any, UserInfo>('/auth/profile')
      console.log('获取用户信息成功:', response)
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }
}

export default api 