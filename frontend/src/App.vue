<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import LoginModal from "./components/LoginModal.vue";
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
            <a class="navbar-item" id="homeRouterButton">
              <RouterLink to="/">Home</RouterLink>
            </a>
            <a class="navbar-item" id="vaultRouterButton">
              <RouterLink to="/vault">Vault</RouterLink>
            </a>
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
.browser {
  width: 100%;
  height: 100%;
}
</style>
