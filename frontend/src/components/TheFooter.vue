<template>
  <footer>
    <div class="footer-container">
      <div class="footer-icons">
        <div class="footer-icon">
          <a
            href="https://www.github.com/jakeyjakeyy/password_manager"
            target="_blank"
            aria-label="GitHub"
          >
            <v-icon name="bi-github" scale="1.25" />
          </a>
        </div>
      </div>
      <div class="footer-version">v1.0.0</div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  background-color: var(--bulma-background);
  color: var(--bulma-text-color);
  padding: 1rem;
  width: 100%;
  height: 3.5rem;
}

.footer-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
}

.footer-icons {
  display: flex;
  justify-content: center;
  flex-grow: 1;
}

.footer-version {
  margin-left: auto;
}
</style>
