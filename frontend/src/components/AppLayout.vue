<template>
  <el-container class="common-layout">
    <el-header class="app-header">
      <el-menu
        :default-active="activeMenu"
        class="el-menu-demo"
        mode="horizontal"
        :router="true"
      >
        <el-menu-item index="/">Home</el-menu-item>
        <el-menu-item index="/upload">Upload</el-menu-item>
        <el-menu-item index="/history">History</el-menu-item>
        
        <div class="menu-right">
          <el-menu-item v-if="!authStore.isAuthenticated" index="/login">Login</el-menu-item>
          <el-sub-menu v-if="authStore.isAuthenticated" index="user-menu">
            <template #title>{{ authStore.username || 'Admin' }}</template>
            <el-menu-item index="/account">Account Settings</el-menu-item>
            <div class="el-menu-item theme-switcher">
              <span>Dark Mode</span>
              <el-switch
                :model-value="themeStore.theme === 'dark'"
                @change="themeStore.toggleTheme"
                inline-prompt
                :active-icon="Moon"
                :inactive-icon="Sunny"
              />
            </div>
            <el-menu-item @click="handleLogout">Logout</el-menu-item>
          </el-sub-menu>
        </div>
      </el-menu>
    </el-header>
    <el-main class="app-main">
      <slot></slot>
    </el-main>
    <el-footer class="app-footer">
      Static Web Hosting Service &copy; 2025 | Version: {{ appVersion }}
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';
import { ElMessage } from 'element-plus';
import { Sunny, Moon } from '@element-plus/icons-vue';

const appVersion = __APP_VERSION__; // Injected by Vite

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
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
}
.el-menu-demo {
  border-bottom: none;
  display: flex;
}
.menu-right {
  margin-left: auto;
}
.app-main {
  flex: 1;
}
.app-footer {
  text-align: center;
  padding: 20px;
  color: var(--el-text-color-secondary);
}

.theme-switcher {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 20px;
}

.theme-switcher span {
  margin-right: 10px;
}
</style>
