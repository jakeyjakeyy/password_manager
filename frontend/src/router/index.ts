import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import VaultView from "../views/VaultView.vue";
import RecoveryView from "../views/RecoveryView.vue";

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
      path: "/vault",
      name: "vault",
      component: VaultView,
    },
    {
      path: "/recovery",
      name: "recovery",
      component: RecoveryView,
    },
  ],
});

export default router;
