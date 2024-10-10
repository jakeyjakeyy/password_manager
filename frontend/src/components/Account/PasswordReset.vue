<script setup lang="ts">
import { ref } from "vue";
import { useCookies } from "vue3-cookies";
import { decryptPassword, decryptFile } from "@/utils/Cryptography";
import { Retrieve } from "@/utils/VaultEntry";
const { cookies } = useCookies();
const serverURL = import.meta.env.VITE_BACKEND_URL;
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const loading = ref(false);

async function resetPassword() {
  const res = await fetch(`${serverURL}/api/recovery/password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    }),
  });
  if (res.ok) {
    // Begin process of reencrypting vault entries
    loading.value = true;
    // Retrieve vault entries
    const vaultEntries = await Retrieve();
    let decryptedEntries = [];
    for (const entry of vaultEntries) {
      // Decrypt password
      const decryptedPassword = await decryptPassword(entry.password, entry.iv);
      decryptedEntries.push({
        ...entry,
        password: decryptedPassword,
      });
    }
    console.log(decryptedEntries);
  } else {
    alert("Failed to reset password. Please try again.");
  }
}
</script>

<template>
  <div v-if="!loading" class="reset-password-container">
    <h1 class="title">Reset Password</h1>
    <form @submit.prevent>
      <div class="field">
        <label class="label">Old Password</label>
        <div class="control">
          <input
            class="input"
            type="password"
            placeholder="Old Password"
            v-model="oldPassword"
          />
        </div>
      </div>
      <div class="field">
        <label class="label">New Password</label>
        <div class="control">
          <input
            class="input"
            type="password"
            placeholder="New Password"
            v-model="newPassword"
          />
        </div>
      </div>
      <div class="field">
        <label class="label">Confirm Password</label>
        <div class="control">
          <input
            class="input"
            type="password"
            placeholder="Confirm Password"
            v-model="confirmPassword"
          />
        </div>
      </div>
      <div class="field">
        <button
          v-if="!oldPassword || !newPassword || !confirmPassword"
          class="button is-primary is-fullwidth"
          disabled
        >
          Reset Password
        </button>
        <button
          v-else
          class="button is-primary is-fullwidth"
          @click="resetPassword"
        >
          Reset Password
        </button>
      </div>
    </form>
  </div>
  <div v-else class="loading-container">
    <!-- <Loading /> -->
    <p>Loading...</p>
  </div>
</template>

<style scoped>
.reset-password-container {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: 100%;
}
</style>
