<script setup lang="ts">
import { onMounted } from "vue";
import Welcome from "@/components/Home/Welcome.vue";
import LoginModal from "@/components/LoginModal.vue";
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
    <LoginModal cta="true" />
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 10%;
  height: 100%;
}
</style>
