<template>
  <footer>
    <div class="footer-container">
      <div class="footer-icons">
        <div class="footer-icon">
          <a
            href="https://www.github.com/jakeyjakeyy/password_manager"
            target="_blank"
          >
            <v-icon name="bi-github" scale="1.25" />
          </a>
        </div>
      </div>
      <div class="footer-version">unreleased</div>
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
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.footer-version {
  position: absolute;
  right: 1rem;
}
</style>
