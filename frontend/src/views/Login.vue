<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="card-header">系统登录</h2>
      </template>
      
      <el-form
        ref="formRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="authStore.loading"
            class="submit-btn"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <el-alert
        v-if="authStore.error"
        :title="authStore.error"
        type="error"
        show-icon
        class="error-alert"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()

const loginForm = ref({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能小于3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  console.log('=== 开始登录流程 ===')
  if (!formRef.value) {
    console.warn('表单引用不存在')
    return
  }
  
  try {
    console.log('验证表单数据')
    const valid = await formRef.value.validate()
    console.log('表单验证结果:', valid)
    
    if (valid) {
      console.log('表单验证通过，提交登录请求')
      console.log('登录表单数据:', loginForm.value)
      
      const success = await authStore.login(loginForm.value)
      console.log('登录请求结果:', success)
      
      if (success) {
        console.log('登录成功，准备跳转')
        ElMessage.success('登录成功')
        router.push('/profile')
      } else {
        console.error('登录失败')
        ElMessage.error(authStore.error || '登录失败')
      }
    } else {
      console.warn('表单验证失败')
      ElMessage.warning('请检查输入')
    }
  } catch (error) {
    console.error('登录过程出错:', error)
    ElMessage.error('登录过程出现错误')
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  
  .login-card {
    width: 400px;
    
    .card-header {
      text-align: center;
      margin: 0;
      color: #303133;
    }
    
    .submit-btn {
      width: 100%;
    }
    
    .error-alert {
      margin-top: 20px;
    }
  }
}
</style> 