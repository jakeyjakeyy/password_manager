<script setup lang="ts">
import { onMounted } from "vue";
import Welcome from "@/components/Home/Welcome.vue";
import HowItWorks from "@/components/Home/HowItWorks.vue";
import Source from "@/components/Home/Source.vue";
onMounted(() => {
  const navRouterButtons = document.querySelectorAll(".navbar-item");
  navRouterButtons.forEach((button) => {
    if (button.id === "homeRouterButton") button.classList.add("is-active");
    else button.classList.remove("is-active");
  });
});
</script>

<template>
  <div class="home-container">
    <Welcome />
    <HowItWorks />
    <Source />
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 10%;
  min-height: 100vh;
  height: fit-content;
  background-image: linear-gradient(
    to right bottom,
    var(--bulma-background) 40%,
    var(--bulma-background-active) 70%
  );
}

@media (max-width: 768px) {
  .home-container {
    padding: 0 1rem;
  }
}
</style>
