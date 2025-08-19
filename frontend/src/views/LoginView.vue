<template>
  <div class="page-container">
    <h1>Admin Login</h1>
    <el-form label-width="120px" @submit.prevent="handleLogin">
      <el-form-item label="Username">
        <el-input v-model="username"></el-input>
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" v-model="password" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="authStore.loading">Login</el-button>
      </el-form-item>
    </el-form>
    <el-alert v-if="authStore.error" :title="authStore.error" type="error" show-icon></el-alert>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value);
  if (success) {
    router.push({ name: 'upload' }); // Redirect to upload page on successful login
  }
};
</script>

<style scoped>
/* Styles for LoginView */
</style>
