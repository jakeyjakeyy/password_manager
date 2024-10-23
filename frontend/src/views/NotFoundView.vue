<script setup lang="ts"></script>

<template>
  <div class="not-found-container">
    <div class="not-found">
      <h1 class="title">404</h1>
      <h2 class="subtitle">Page not found</h2>
      <router-link to="/">Go to Home</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
}
</style>
