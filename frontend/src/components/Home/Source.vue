<script setup lang="ts"></script>

<template>
  <div class="source-container">
    <div class="header">
      <div class="header-title">
        <h1 class="title is-1">Source Code</h1>
      </div>
      <div class="header-content">
        <p class="subtitle is-4">Request a feature, report a bug, and more.</p>
      </div>
      <div class="source-content">
        <p class="subtitle is-5">
          This project is open-source, and welcomes contributions from the
          community. You can find the source code, submit issues, and contribute
          <span
            ><a
              href="https://github.com/jakeyjakeyy/password_manager"
              target="_blank"
              >on GitHub</a
            ></span
          >.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.source-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  min-height: 25vh;
  padding: 0 15%;
  margin-top: 5rem;
  margin-bottom: 3rem;
}

.source-content {
  text-align: center;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

a {
  font-weight: bold;
  border-bottom: 2px solid var(--bulma-primary);
}
</style>
