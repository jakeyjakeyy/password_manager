import { createRouter, createWebHistory } from "vue-router";
const HomeView = () => import("../views/HomeView.vue");
const AboutView = () => import("../views/AboutView.vue");
const AccountView = () => import("../views/AccountView.vue");
const SettingsView = () => import("../views/SettingsView.vue");
const VaultView = () => import("../views/VaultView.vue");
const RecoveryView = () => import("../views/RecoveryView.vue");
const NotFoundView = () => import("../views/NotFoundView.vue");

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
    },
    {
      path: "/account",
      name: "account",
      component: AccountView,
    },
    {
      path: "/settings",
      name: "settings",
      component: SettingsView,
    },
    {
      path: "/vault",
      name: "vault",
      component: VaultView,
    },
    {
      path: "/recovery",
      name: "recovery",
      component: RecoveryView,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundView,
    },
  ],
});

export default router;
