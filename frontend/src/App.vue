<script setup>
import AppLayout from "./components/AppLayout.vue";
</script>

<template>
  <AppLayout>
    <RouterView />
  </AppLayout>
</template>

<style>
/* Global styles to make the theme work across the app */
body {
  margin: 0;
  padding: 0;
  background-color: var(--el-bg-color);
  color: var(--el-text-color-primary);
  transition:
    background-color 0.2s ease-in-out,
    color 0.2s ease-in-out;
}
</style>
