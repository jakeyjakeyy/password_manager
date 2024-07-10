<script setup lang="ts">
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
import LoginModal from "@/components/LoginModal.vue";
import RefreshToken from "@/utils/RefreshToken";
const serverURL = import.meta.env.VITE_BACKEND_URL;
</script>

<template>
  <main>
    <h1>Home</h1>
    <LoginModal />
  </main>
</template>
