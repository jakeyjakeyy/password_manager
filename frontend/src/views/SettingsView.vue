<script setup lang="ts">
import ThemeSelector from "@/components/Settings/ThemeSelector.vue";
import { onMounted } from "vue";
onMounted(() => {
  document.title = "Settings";
});
</script>

<template>
  <div class="settings-container">
    <div class="header">
      <h1 class="title">Settings</h1>
    </div>
    <div class="content">
      <ThemeSelector />
    </div>
  </div>
</template>

<style scoped>
.settings-container {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: 100%;
  margin-top: 2rem;
  padding: 0 25%;
  gap: 2rem;
}
</style>
