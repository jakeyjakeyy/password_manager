<script setup lang="ts">
import { onMounted } from "vue";
import Welcome from "@/components/Home/Welcome.vue";
import LoginModal from "@/components/LoginModal.vue";
import HowItWorks from "@/components/Home/HowItWorks.vue";
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
}

@media (max-width: 768px) {
  .home-container {
    padding: 0 1rem;
  }
}
</style>
