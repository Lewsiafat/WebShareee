<template>
  <el-container class="common-layout">
    <el-aside class="app-aside" width="200px">
      <div class="brand-logo">
        <a href="/" class="logo-link">
          <img src="../assets/logo.svg" alt="Brand Logo" class="logo-img" />
          <span class="logo-text">Static Web</span>
        </a>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        :router="true"
        :collapse="isCollapsed"
      >
        <el-menu-item index="/">
          <el-icon><home-filled /></el-icon>
          <span>Home</span>
        </el-menu-item>
        <el-menu-item index="/upload">
          <el-icon><upload-filled /></el-icon>
          <span>Upload</span>
        </el-menu-item>
        <el-menu-item index="/history">
          <el-icon><data-line /></el-icon>
          <span>History</span>
        </el-menu-item>
      </el-menu>
      <div class="aside-footer">
        <div class="theme-switcher-container">
          <el-switch
            :model-value="themeStore.theme === 'dark'"
            @change="themeStore.toggleTheme"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
          />
          <span v-if="!isCollapsed" class="theme-text">Dark Mode</span>
        </div>
      </div>
    </el-aside>
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="header-left">
            <el-icon @click="isCollapsed = !isCollapsed" class="collapse-icon">
              <expand v-if="isCollapsed" />
              <fold v-else />
            </el-icon>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }"
                >Homepage</el-breadcrumb-item
              >
              <el-breadcrumb-item
                ><a href="/">Activity management</a></el-breadcrumb-item
              >
              <el-breadcrumb-item>promote list</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="menu-right">
            <el-menu-item
              v-if="!authStore.isAuthenticated"
              index="/login"
              :router="true"
              >Login</el-menu-item
            >
            <el-sub-menu v-if="authStore.isAuthenticated" index="user-menu">
              <template #title>
                <el-avatar
                  size="small"
                  :src="authStore.avatarUrl || defaultAvatar"
                  class="user-avatar"
                />
                <span>{{ authStore.username || "Admin" }}</span>
              </template>
              <el-menu-item index="/account">Account Settings</el-menu-item>
              <el-menu-item @click="handleLogout">Logout</el-menu-item>
            </el-sub-menu>
          </div>
        </div>
      </el-header>
      <el-main class="app-main">
        <slot></slot>
      </el-main>
      <el-footer class="app-footer">
        <div class="footer-content">
          <span
            >Static Web Hosting Service &copy; 2025 | Version:
            {{ appVersion }}</span
          >
          <div class="social-links">
            <a href="#" target="_blank" aria-label="Github Link"
              ><el-icon><platform /></el-icon
            ></a>
            <a href="#" target="_blank" aria-label="Twitter Link"
              ><el-icon><promotion /></el-icon
            ></a>
            <a href="#" target="_blank" aria-label="LinkedIn Link"
              ><el-icon><position /></el-icon
            ></a>
          </div>
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useThemeStore } from "../stores/theme";
import { ElMessage } from "element-plus";
import {
  Sunny,
  Moon,
  HomeFilled,
  UploadFilled,
  DataLine,
  Expand,
  Fold,
  Platform,
  Promotion,
  Position,
} from "@element-plus/icons-vue";
import defaultAvatar from "../assets/default-avatar.png";

const appVersion = __APP_VERSION__;

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const activeMenu = ref(route.path);
const isCollapsed = ref(false);

watch(
  () => route.path,
  (newPath) => {
    activeMenu.value = newPath;
  },
);

const handleLogout = () => {
  authStore.logout();
  ElMessage.success("Logged out successfully!");
  router.push({ name: "home" });
};
</script>

<style scoped>
.common-layout {
  height: 100vh;
}

.app-aside {
  border-right: 1px solid var(--el-border-color);
  transition: width 0.3s;
  display: flex;
  flex-direction: column;
}

.el-menu {
  flex-grow: 1;
}

.aside-footer {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.theme-switcher-container {
  display: flex;
  align-items: center;
}

.theme-text {
  margin-left: 10px;
  color: var(--el-text-color-regular);
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  background-color: transparent;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--el-text-color-primary);
}

.logo-img {
  height: 32px;
  width: 32px;
  margin-right: 10px;
}

.logo-text {
  font-weight: 600;
  font-size: 20px;
}

.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--el-border-color);
  height: 60px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-icon {
  font-size: 20px;
  cursor: pointer;
  margin-right: 15px;
}

.menu-right {
  display: flex;
  align-items: center;
}

.user-avatar {
  margin-right: 10px;
}

.app-main {
  padding: 20px;
}

.app-footer {
  padding: 0 20px;
  color: var(--el-text-color-secondary);
  border-top: 1px solid var(--el-border-color);
  height: 60px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.social-links {
  display: flex;
  align-items: center;
}

.social-links a {
  color: var(--el-text-color-secondary);
  margin-left: 15px;
  font-size: 20px;
  transition: color 0.3s;
}

.social-links a:hover {
  color: var(--el-color-primary);
}
</style>
