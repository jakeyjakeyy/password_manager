<script setup lang="ts">
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
import LoginModal from "@/components/LoginModal.vue";
const serverURL = import.meta.env.VITE_BACKEND_URL;

async function handleClick() {
  const access = cookies.get("access_token");
  console.log(access);
  const salt = await fetch(`${serverURL}/api/salt`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${access}`,
    },
  }).then((response) => response.json());
}
</script>

<template>
  <main>
    <h1>Home</h1>
    <LoginModal />
    <button class="button" @click="handleClick">Click me</button>
  </main>
</template>
