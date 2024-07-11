<script setup lang="ts">
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
import LoginModal from "@/components/LoginModal.vue";
import RefreshToken from "@/utils/RefreshToken";
const serverURL = import.meta.env.VITE_BACKEND_URL;
import * as Cryptography from "@/utils/Cryptography";

async function handleClick() {
  // blabla
  const key = await Cryptography.retrieveKey();
  const password = "test";
  const encrypted = await Cryptography.encryptPassword(password, key);
  console.log(encrypted);
  const decrypted = await Cryptography.decryptPassword(
    encrypted.encryptedPassword,
    encrypted.iv,
    key
  );
  console.log(decrypted);
}
</script>

<template>
  <main>
    <h1>Home</h1>
    <LoginModal />
    <button class="button" @click="handleClick">Click me</button>
  </main>
</template>
