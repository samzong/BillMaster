import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token'),
    username: localStorage.getItem('username')
  }),
  
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username,
          password
        })
        
        this.token = response.data.token
        this.username = response.data.username
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('username', this.username)
        
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },
    
    async changePassword(oldPassword, newPassword) {
      try {
        await axios.post('http://localhost:5000/api/change_password', 
          {
            old_password: oldPassword,
            new_password: newPassword
          },
          {
            headers: { Authorization: `Bearer ${this.token}` }
          }
        )
        return true
      } catch (error) {
        console.error('Change password failed:', error)
        return false
      }
    },
    
    logout() {
      this.token = null
      this.username = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
}) 