import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/upload",
      name: "upload",
      component: () => import("../views/UploadView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/history",
      name: "history",
      component: () => import("../views/HistoryView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/account",
      name: "account",
      component: () => import("../views/AccountView.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  // const authStore = useAuthStore();
  // if (to.meta.requiresAuth && !authStore.isAuthenticated) {
  //   next({ name: 'login' });
  // } else if (to.name === 'login' && authStore.isAuthenticated) {
  //   next({ name: 'home' }); // Redirect to home if already logged in and trying to access login page
  // } else {
  //   next();
  // }
  next(); // TEMPORARY: Bypass authentication for development
});

export default router;
