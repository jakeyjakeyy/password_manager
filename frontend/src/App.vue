<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import LoginModal from "./components/LoginModal.vue";
import TheFooter from "./components/TheFooter.vue";
import { onMounted, ref } from "vue";
const username = ref<string | null>(null);

// Theme initialization
const theme = localStorage.getItem("theme");
if (theme) {
  document.documentElement.setAttribute(
    "data-theme",
    localStorage.getItem("theme") || ""
  );
} else {
  window.matchMedia("(prefers-color-scheme: dark)").matches
    ? document.documentElement.setAttribute("data-theme", "dark")
    : document.documentElement.setAttribute("data-theme", "light");
}

document.addEventListener("DOMContentLoaded", () => {
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      el.classList.toggle("is-active");
      $target?.classList.toggle("is-active");
    });
  });
});

onMounted(() => {
  setInterval(() => {
    if (localStorage.getItem("username")) {
      username.value = localStorage.getItem("username");
    } else {
      username.value = null;
    }
  }, 100);
});
</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="navbar" aria-label="main navigation">
        <a
          role="button"
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-main"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
        <div id="navbar-main" class="navbar-menu">
          <div class="navbar-start">
            <RouterLink to="/" class="navbar-item" id="homeRouterButton"
              >Home</RouterLink
            >
            <RouterLink to="/vault" class="navbar-item" id="vaultRouterButton"
              >Vault</RouterLink
            >
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">More</a>
              <div class="navbar-dropdown">
                <RouterLink to="/account" class="navbar-item"
                  >Account</RouterLink
                >
                <RouterLink to="/settings" class="navbar-item"
                  >Settings</RouterLink
                >
                <hr class="navbar-divider" />
                <a
                  class="navbar-item"
                  href="https://github.com/jakeyjakeyy/password_manager/issues"
                  target="_blank"
                  >Report an issue</a
                >
              </div>
            </div>
          </div>
          <div class="navbar-end">
            <LoginModal />
          </div>
        </div>
      </nav>
    </div>
  </header>

  <div class="browser">
    <RouterView />
    <TheFooter />
  </div>
</template>

<style scoped>
header {
  position: fixed;
  z-index: 1000;
}
.browser {
  padding-top: 3.25rem;
  width: 100%;
  height: 100%;
  overflow: auto;
}
a {
  color: var(--bulma-text);
}
.is-active {
  background-color: var(--bulma-background-color);
  border: var(--bulma-primary) 1px solid;
  color: var(--bulma-primary);
}

.navbar {
  width: 100vw;
  padding: 0 1rem;
}
</style>
