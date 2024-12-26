<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人中心</h2>
          <el-button type="danger" @click="handleLogout">退出登录</el-button>
        </div>
      </template>

      <div v-if="authStore.loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <template v-else>
        <div v-if="authStore.user" class="user-info">
          <h3>用户信息</h3>
          <p><strong>用户名：</strong>{{ authStore.user.username }}</p>
          <p><strong>邮箱：</strong>{{ authStore.user.email || "未设置" }}</p>
          <p>
            <strong>注册时间：</strong
            >{{ formatDate(authStore.user.created_at) }}
          </p>
        </div>

        <el-divider />

        <div class="change-password">
          <h3>修改密码</h3>
          <el-form
            ref="formRef"
            :model="passwordForm"
            :rules="rules"
            label-position="top"
            @submit.prevent="handleChangePassword"
          >
            <el-form-item label="原密码" prop="oldPassword">
              <el-input
                v-model="passwordForm.oldPassword"
                type="password"
                placeholder="请输入原密码"
                show-password
              />
            </el-form-item>

            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>

            <el-form-item label="确认新密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                native-type="submit"
                :loading="authStore.loading"
              >
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </template>

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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const formRef = ref<FormInstance>();

const passwordForm = ref({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value !== passwordForm.value.newPassword) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const rules: FormRules = {
  oldPassword: [
    { required: true, message: "请输入原密码", trigger: "blur" },
    { min: 6, message: "密码长度不能小于6个字符", trigger: "blur" },
  ],
  newPassword: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 6, message: "密码长度不能小于6个字符", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "请再次输入新密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
};

const handleChangePassword = async () => {
  if (!formRef.value) return;

  try {
    const valid = await formRef.value.validate();
    if (valid) {
      const success = await authStore.changePassword({
        old_password: passwordForm.value.oldPassword,
        new_password: passwordForm.value.newPassword,
      });

      if (success) {
        ElMessage.success("密码修改成功");
        passwordForm.value = {
          oldPassword: "",
          newPassword: "",
          confirmPassword: "",
        };
      }
    }
  } catch (error) {
    console.error("修改密码失败:", error);
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push("/login");
  ElMessage.success("已退出登录");
};

const formatDate = (dateString?: string) => {
  if (!dateString) return "未知";
  return new Date(dateString).toLocaleString();
};

onMounted(async () => {
  if (!authStore.token) {
    router.push("/login");
    return;
  }

  try {
    await authStore.getProfile();
  } catch (error) {
    console.error("获取用户信息失败:", error);
    router.push("/login");
  }
});
</script>

<style scoped lang="scss">
.profile-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;

  .profile-card {
    max-width: 600px;
    margin: 0 auto;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h2 {
        margin: 0;
        color: #303133;
      }
    }

    .loading-container {
      padding: 20px 0;
    }

    .user-info {
      margin-bottom: 20px;

      h3 {
        color: #303133;
        margin-bottom: 15px;
      }

      p {
        margin: 10px 0;
        color: #606266;
      }
    }

    .change-password {
      h3 {
        color: #303133;
        margin-bottom: 15px;
      }
    }

    .error-alert {
      margin-top: 20px;
    }
  }
}
</style>
