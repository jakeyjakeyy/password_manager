<script setup lang="ts">
import { ref } from "vue";
import { useCookies } from "vue3-cookies";
import { useRouter } from "vue-router";
import * as cryptography from "@/utils/Cryptography";
import * as account from "@/utils/Account";
import { Retrieve } from "@/utils/VaultEntry";
const { cookies } = useCookies();
const router = useRouter();
const serverURL = import.meta.env.VITE_BACKEND_URL;
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const recoverySecret = ref("");
const recoveryUrl = ref("");
const progress = ref(0);

async function resetPassword() {
  // Begin process of reencrypting vault entries
  loading.value = true;
  progress.value = 0;

  // Retrieve vault entries
  const vaultEntries = await Retrieve();
  let decryptedEntries = [];
  progress.value = 10;

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
  progress.value = 30;

  // Get account's salt
  const salt = await account.getSalt();
  // Derive new key from new password
  const newKey = await cryptography.deriveKey(newPassword.value, salt);
  await cryptography.storeKey(newKey);
  progress.value = 40;

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
  progress.value = 60;

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
    progress.value = 70;
    recoverySecret.value = cryptography.generateRecoverySecret();
    const blob = new Blob([recoverySecret.value], { type: "text/plain" });
    recoveryUrl.value = URL.createObjectURL(blob);

    // Call recovery/password endpoint
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
      progress.value = 90;
      const salt = await account.getSalt();
      await account.confirmRecovery(
        recoverySecret.value,
        newPassword.value,
        salt
      );
      progress.value = 100;
      const modal = document.getElementById("passwordResetModal");
      modal?.classList.add("is-active");
    } else {
      alert("Failed to reset password. Please try again.");
    }
  } else {
    alert("Failed to reset password. Please try again.");
  }
  loading.value = false;
}

async function closeModal() {
  const modal = document.getElementById("passwordResetModal");
  modal?.classList.remove("is-active");
  loading.value = false;
  await account.handleLogout();
  router.push("/");
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
        <progress
          v-if="loading"
          class="progress is-primary"
          :value="progress"
          max="100"
        >
          {{ progress }}%
        </progress>
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

    <!-- Modal -->
    <div class="modal" id="passwordResetModal">
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">
          <h1 class="title">Recovery Secret</h1>
          <p>
            Resetting your password also creates a new recovery secret. Please
            download this secret and store it in a safe place.
          </p>
          <a
            :href="recoveryUrl"
            download="vault-recovery-secret.txt"
            @click="closeModal()"
          >
            <button class="button is-primary is-fullwidth">Download</button>
          </a>
        </div>
        <button
          class="modal-close is-large"
          aria-label="close"
          @click="closeModal"
        ></button>
      </div>
    </div>
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
