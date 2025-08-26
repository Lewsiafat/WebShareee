<template>
  <el-container class="common-layout">
    <el-header class="app-header">
      <el-menu
        :default-active="activeMenu"
        class="el-menu-demo"
        mode="horizontal"
        :router="true"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="/">Home</el-menu-item>
        <el-menu-item index="/upload">Upload</el-menu-item>
        <el-menu-item index="/history">History</el-menu-item>
        <el-menu-item index="/login" style="margin-left: auto;">Login</el-menu-item>
        <!-- Add logout button if authenticated -->
        <el-sub-menu v-if="authStore.isAuthenticated" index="user-menu" style="margin-left: auto;">
          <template #title>{{ authStore.username || 'Admin' }}</template>
          <el-menu-item index="/account">帳號設定</el-menu-item>
          <el-menu-item @click="handleLogout">Logout</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-header>
    <el-main class="app-main">
      <slot></slot>
    </el-main>
    <el-footer class="app-footer">
      Static Web Hosting Service &copy; 2025
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { ElMessage } from 'element-plus';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const activeMenu = ref(route.path);

watch(
  () => route.path,
  (newPath) => {
    activeMenu.value = newPath;
  }
);

const handleLogout = () => {
  authStore.logout();
  ElMessage.success('Logged out successfully!');
  router.push({ name: 'home' });
};
</script>

<style scoped>
.common-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  padding: 0;
  border-bottom: 1px solid #eee;
}
.el-menu-demo {
  border-bottom: none;
}
.app-main {
  flex: 1;
  padding: 20px;
  background-color: #f9fafc;
}
.app-footer {
  text-align: center;
  padding: 20px;
  color: #666;
  border-top: 1px solid #eee;
  background-color: #f0f2f5;
}
</style>
