<script setup lang="ts">
import { onMounted } from "vue";
onMounted(() => {
  const navRouterButtons = document.querySelectorAll(".navbar-item");
  navRouterButtons.forEach((button) => {
    if (button.id === "homeRouterButton") button.classList.add("is-active");
    else button.classList.remove("is-active");
  });
});
</script>

<template>
  <main>
    <h1>Home</h1>
  </main>
</template>
