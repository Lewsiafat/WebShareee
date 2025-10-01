import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useThemeStore = defineStore("theme", () => {
  // State: Initialize theme from localStorage or default to 'light'
  const theme = ref(localStorage.getItem("theme") || "light");

  // Action: Toggle theme between 'light' and 'dark'
  function toggleTheme() {
    theme.value = theme.value === "light" ? "dark" : "light";
  }

  // Watch for changes and update the <html> element and localStorage
  watch(theme, (newTheme) => {
    if (newTheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", newTheme);
  });

  // Function to apply initial theme on app load
  function applyInitialTheme() {
    if (theme.value === "dark") {
      document.documentElement.classList.add("dark");
    }
  }

  return { theme, toggleTheme, applyInitialTheme };
});
