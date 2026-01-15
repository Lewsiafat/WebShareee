<template>
  <div class="login-container">
    <div class="login-card glass-panel">
      <div class="login-header">
        <div class="icon-wrapper">
          <img src="../assets/logo.svg" alt="Logo" class="login-logo" />
        </div>
        <h1>Welcome Back</h1>
        <p class="subtitle">Enter your credentials to access the admin dashboard</p>
      </div>

      <el-form 
        label-position="top" 
        @submit.prevent="handleLogin" 
        size="large"
        class="login-form"
      >
        <el-form-item label="Username">
          <el-input 
            v-model="username" 
            placeholder="admin"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="Password">
          <el-input 
            type="password" 
            v-model="password" 
            show-password 
            placeholder="••••••••"
            :prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="full-width-btn"
            native-type="submit"
            :loading="authStore.loading"
          >
            Sign In
          </el-button>
        </el-form-item>
      </el-form>

      <el-alert
        v-if="authStore.error"
        :title="authStore.error"
        type="error"
        show-icon
        :closable="false"
        class="login-alert"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { User, Lock } from "@element-plus/icons-vue";

const username = ref("");
const password = ref("");
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value);
  if (success) {
    router.push({ name: "upload" });
  }
};
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 140px); /* Adjust for header/footer */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.85); /* Slightly more opaque for readability */
}

.dark .login-card {
  background: rgba(30, 41, 59, 0.85);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.icon-wrapper {
  width: 64px;
  height: 64px;
  background: rgba(79, 70, 229, 0.1);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.login-logo {
  width: 32px;
  height: 32px;
}

h1 {
  font-size: 24px;
  margin-bottom: 8px;
  color: var(--text-main);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.login-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-main);
}

.full-width-btn {
  width: 100%;
  margin-top: 10px;
  height: 44px;
  font-size: 16px;
}

.login-alert {
  margin-top: 20px;
  border-radius: 8px;
}
</style>
