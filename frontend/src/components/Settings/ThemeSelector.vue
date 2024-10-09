<script setup lang="ts">
import { onMounted, ref } from "vue";
const theme = ref("");

onMounted(() => {
  document.documentElement.getAttribute("data-theme") === "dark"
    ? (theme.value = "dark")
    : (theme.value = "light");
});

function themeSelect(selectedTheme: string) {
  document.documentElement.setAttribute("data-theme", selectedTheme);
  theme.value = selectedTheme;
  localStorage.setItem("theme", selectedTheme);
}
</script>

<template>
  <div class="theme-selector-container">
    <h1 class="title">Theme Selector</h1>
    <div class="theme-selector">
      <div class="theme">
        <h2 class="subtitle">Light</h2>
        <button
          v-if="theme !== 'light'"
          class="button is-primary"
          @click="themeSelect('light')"
        >
          Select
        </button>
        <button v-else class="button is-primary" disabled>Selected</button>
      </div>
      <div class="theme">
        <h2 class="subtitle">Dark</h2>
        <button
          v-if="theme !== 'dark'"
          class="button is-primary"
          @click="themeSelect('dark')"
        >
          Select
        </button>
        <button v-else class="button is-primary" disabled>Selected</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.theme-selector {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  margin-top: 2rem;
  gap: 2rem;
}
</style>
