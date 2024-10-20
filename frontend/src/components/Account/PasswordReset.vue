<script setup lang="ts">
import { ref } from "vue";
import { useCookies } from "vue3-cookies";
import * as cryptography from "@/utils/Cryptography";
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
    // Decrypt vault entries and their files
    for (const entry of vaultEntries) {
      let files = [];
      // Decrypt password
      const decryptedPassword = await cryptography.decryptPassword(
        entry.password,
        entry.iv
      );
      for (const file of entry.files) {
        const decryptedFile = await cryptography.decryptFile(
          file.file,
          file.iv,
          file.name
        );
        const url = URL.createObjectURL(decryptedFile);
        let fileObj = { file: decryptedFile, url: url, id: file.id };
        files.push(fileObj);
      }
      decryptedEntries.push({
        ...entry,
        password: decryptedPassword,
        files: files,
      });
    }
    // Get account's salt
    const saltResponse = await fetch(`${serverURL}/api/salt`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
    });
    const saltData = await saltResponse.json();
    const salt = saltData.salt;
    // Derive new key from new password
    const newKey = await cryptography.deriveKey(newPassword.value, salt);
    await cryptography.storeKey(newKey);
    // Reencrypt vault entries
    let encryptedEntries = [];
    let encryptedFiles = [];
    for (const entry of decryptedEntries) {
      const encryptedPassword = await cryptography.encryptPassword(
        entry.password
      );
      entry.password = encryptedPassword.encryptedPassword;
      entry.iv = encryptedPassword.iv;
      for (const file of entry.files) {
        const encryptedFile = await cryptography.encryptFile(file.file);
        encryptedFiles.push({
          file: encryptedFile.encryptedFile,
          iv: encryptedFile.iv,
          name: file.file.name,
          id: file.id,
        });
      }
      entry.files = encryptedFiles;
      encryptedEntries.push(entry);
    }

    // Send reencrypted vault entries to server
    const batchRes = await fetch(`${serverURL}/api/vault/edit-batch`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
      body: JSON.stringify({
        entries: encryptedEntries,
      }),
    });
    if (batchRes.ok) {
      alert("Password reset successfully.");
    } else {
      alert("Failed to reset password. Please try again.");
    }
    loading.value = false;
  } else {
    alert("Failed to reset password. Please try again.");
  }
}
</script>

<template>
  <div class="reset-password-container">
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
          :class="[
            'button',
            'is-primary',
            'is-fullwidth',
            { 'is-skeleton': loading },
          ]"
          @click="resetPassword"
        >
          Reset Password
        </button>
      </div>
    </form>
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
