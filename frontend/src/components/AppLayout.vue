<template>
  <el-container class="common-layout">
    <el-aside class="app-aside glass-panel" :width="isCollapsed ? '64px' : '260px'">
      <div class="brand-logo" :class="{ collapsed: isCollapsed }">
        <a href="/" class="logo-link">
          <div class="logo-wrapper">
             <img src="../assets/logo.svg" alt="Brand Logo" class="logo-img" />
          </div>
          <span class="logo-text" v-if="!isCollapsed">Static<span class="brand-accent">Web</span></span>
        </a>
      </div>
      
      <div class="menu-container">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          :router="true"
          :collapse="isCollapsed"
          background-color="transparent"
          text-color="var(--text-secondary)"
          active-text-color="var(--brand-primary)"
        >
          <el-menu-item index="/">
            <el-icon><home-filled /></el-icon>
            <template #title>Home</template>
          </el-menu-item>
          <el-menu-item index="/upload">
            <el-icon><upload-filled /></el-icon>
            <template #title>Upload</template>
          </el-menu-item>
          <el-menu-item index="/history">
            <el-icon><data-line /></el-icon>
            <template #title>History</template>
          </el-menu-item>
        </el-menu>
      </div>

      <div class="aside-footer">
        <div class="theme-switcher-container" :class="{ collapsed: isCollapsed }">
          <el-switch
            :model-value="themeStore.theme === 'dark'"
            @change="themeStore.toggleTheme"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            style="--el-switch-on-color: var(--brand-secondary); --el-switch-off-color: #cbd5e1"
          />
          <span v-if="!isCollapsed" class="theme-text">Dark Mode</span>
        </div>
      </div>
    </el-aside>

    <el-container class="main-content-wrapper">
      <el-header class="app-header glass-panel">
        <div class="header-content">
          <div class="left-section">
             <el-icon @click="isCollapsed = !isCollapsed" class="collapse-icon">
              <expand v-if="isCollapsed" />
              <fold v-else />
            </el-icon>
            <h2 class="page-title">{{ currentPageTitle }}</h2>
          </div>
         
          <div class="menu-right">
             <div v-if="!authStore.isAuthenticated" class="auth-buttons">
               <el-button type="primary" round @click="router.push('/login')">Login</el-button>
             </div>
             
             <el-dropdown v-else trigger="click">
                <div class="user-profile">
                   <el-avatar
                    size="small"
                    :src="authStore.avatarUrl || defaultAvatar"
                    class="user-avatar"
                  />
                  <span class="username">{{ authStore.username || "Admin" }}</span>
                  <el-icon><caret-bottom /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu class="user-dropdown">
                    <el-dropdown-item @click="router.push('/account')">Account Settings</el-dropdown-item>
                    <el-dropdown-item divided @click="handleLogout">Logout</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
             </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
      
      <el-footer class="app-footer">
        <div class="footer-content">
          <span class="copyright">
            Static Web Hosting Service &copy; 2025
          </span>
          <div class="social-links">
            <a href="#" target="_blank" aria-label="Github"><el-icon><platform /></el-icon></a>
            <a href="#" target="_blank" aria-label="Twitter"><el-icon><promotion /></el-icon></a>
          </div>
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, watch, computed } from "vue";
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
  CaretBottom
} from "@element-plus/icons-vue";
import defaultAvatar from "../assets/default-avatar.png";

const appVersion = __APP_VERSION__;

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const activeMenu = ref(route.path);
const isCollapsed = ref(false);

const currentPageTitle = computed(() => {
  switch(route.path) {
    case '/': return 'Dashboard';
    case '/upload': return 'Upload New Page';
    case '/history': return 'Page History';
    case '/login': return 'Login';
    case '/account': return 'Account Settings';
    default: return '';
  }
});

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
  background-image: 
    radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.08) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(14, 165, 233, 0.08) 0px, transparent 50%);
}

/* Sidebar Styling */
.app-aside {
  border-right: 1px solid var(--border-light);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  z-index: 20;
}

.brand-logo {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
}

.brand-logo.collapsed {
  padding: 0;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 12px;
}

.logo-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.logo-img {
  height: 24px;
  width: 24px;
}

.logo-text {
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: 20px;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.brand-accent {
  color: var(--brand-primary);
}

.menu-container {
  flex: 1;
  padding: 20px 0;
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  margin: 4px 12px;
  border-radius: 8px;
  height: 48px;
  font-weight: 500;
}

.el-menu-item:hover {
  background-color: var(--el-bg-color-page);
}

.el-menu-item.is-active {
  background: linear-gradient(90deg, rgba(79, 70, 229, 0.1), transparent);
  color: var(--brand-primary);
  border-left: 3px solid var(--brand-primary);
}

.aside-footer {
  padding: 24px;
  border-top: 1px solid var(--border-light);
}

.theme-switcher-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(255,255,255,0.5);
  border-radius: 8px;
}

.theme-switcher-container.collapsed {
  justify-content: center;
  background: transparent;
  padding: 0;
}

.theme-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Header Styling */
.app-header {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 32px;
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.collapse-icon {
  font-size: 20px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s;
}

.collapse-icon:hover {
  color: var(--brand-primary);
}

.page-title {
  font-size: 1.25rem;
  margin: 0;
  color: var(--text-main);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 20px;
  transition: background 0.2s;
}

.user-profile:hover {
  background: rgba(0,0,0,0.05);
}

.username {
  font-weight: 500;
  color: var(--text-main);
}

/* Main Area */
.app-main {
  padding: 32px;
  overflow-y: auto;
}

/* Footer */
.app-footer {
  height: 50px;
  padding: 0 32px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.footer-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-light);
}

.social-links {
  display: flex;
  gap: 16px;
}

.social-links a {
  color: var(--text-secondary);
  font-size: 18px;
  transition: all 0.2s;
}

.social-links a:hover {
  color: var(--brand-primary);
  transform: translateY(-2px);
}
</style>
