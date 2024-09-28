<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import LoginModal from "./components/LoginModal.vue";

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
              <a class="navbar-link">Dropdown</a>
              <div class="navbar-dropdown">
                <a class="navbar-item">Dropdown item</a>
                <a class="navbar-item">Other item</a>
                <hr class="navbar-divider" />
                <a class="navbar-item">Separated link</a>
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
  </div>
</template>

<style scoped>
header {
  position: fixed;
  z-index: 1000;
}
.browser {
  width: 100%;
  height: 100%;
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
