import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi, type LoginData, type ChangePasswordData } from '../api/auth'

interface UserInfo {
  id: number
  username: string
  email: string | null
  created_at: string
  updated_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<UserInfo | null>(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const login = async (loginData: LoginData) => {
    try {
      loading.value = true
      error.value = null
      const response = await authApi.login(loginData)
      
      // 存储 token
      if (response && response.access_token) {
        token.value = response.access_token
        localStorage.setItem('token', response.access_token)
        
        // 存储用户信息
        if (response.user) {
          user.value = response.user
          localStorage.setItem('user', JSON.stringify(response.user))
        }
        
        return true
      }
      
      error.value = '登录响应格式错误'
      return false
    } catch (err: any) {
      console.error('Login error:', err)
      error.value = err.message || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const changePassword = async (data: ChangePasswordData) => {
    try {
      loading.value = true
      error.value = null
      await authApi.changePassword(data)
      return true
    } catch (err: any) {
      error.value = err.message || '修改密码失败'
      return false
    } finally {
      loading.value = false
    }
  }

  const getProfile = async () => {
    try {
      if (!token.value) {
        throw new Error('未登录')
      }
      
      loading.value = true
      error.value = null
      const response = await authApi.getProfile()
      
      if (response) {
        user.value = response
        localStorage.setItem('user', JSON.stringify(response))
        return true
      }
      
      return false
    } catch (err: any) {
      console.error('Get profile error:', err)
      error.value = err.message || '获取用户信息失败'
      
      // 如果是认证错误，清除登录状态
      if (err.status === 401 || err.status === 422) {
        logout()
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    token,
    user,
    loading,
    error,
    login,
    logout,
    changePassword,
    getProfile
  }
}) 