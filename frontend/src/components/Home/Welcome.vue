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

.welcome-header {
  animation: slide-in-left 1s forwards;
}

.welcome-content {
  animation: slide-in-left 1.2s forwards;
}

@media (max-width: 768px) {
  .welcome-container {
    padding: 1rem;
  }
  .title {
    font-size: 3rem;
  }
}

@keyframes slide-in-left {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}
</style>
