<script setup lang="ts"></script>

<template>
  <div class="welcome-container">
    <div class="welcome-header">
      <h1 class="title">Welcome to The Vault</h1>
    </div>
    <div class="welcome-content">
      <p class="subtitle">
        A cryptographically secure password vault and generator designed to keep
        your credentials safe and easily accessible.
      </p>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5% 15%;
  text-align: center;
}

.title {
  font-size: 5rem;
  margin-bottom: 1rem;
  text-align: center;
}
</style>
