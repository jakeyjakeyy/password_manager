<script setup lang="ts">
import { onMounted } from "vue";
import { checkToken } from "@/utils/RefreshToken";
import PasswordReset from "@/components/Account/PasswordReset.vue";

onMounted(() => {
  if (!checkToken()) {
    window.location.href = "/";
  }
  document.title = "Account";
});
</script>

<template>
  <div class="account-container">
    <div class="header">
      <h1 class="title">Account</h1>
    </div>
    <div class="content">
      <PasswordReset />
    </div>
  </div>
</template>

<style scoped>
.account-container {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: 100%;
  margin-top: 2rem;
  padding: 0 25%;
  gap: 2rem;
}
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  font-size: 3rem;
}
</style>
