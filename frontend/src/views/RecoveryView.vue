<script setup lang="ts">
import {
  decryptPassword,
  deleteKey,
  deriveKey,
  storeKey,
  objectToUint8Array,
} from "@/utils/Cryptography";
import { ref } from "vue";
const serverURL = import.meta.env.VITE_BACKEND_URL;
const username = ref("");
const secret = ref("");

async function recover() {
  const response = await fetch(`${serverURL}/api/recovery`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      secret: secret.value,
      verify: true,
    }),
  });
  if (response.ok) {
    const data = await response.json();
    deleteKey();
    const key = await deriveKey(secret.value, data.salt);
    await storeKey(key);
    let encryptedPassword = data.password;
    let decryptedPassword = await decryptPassword(
      objectToUint8Array(encryptedPassword),
      objectToUint8Array(data.iv)
    );
    console.log(decryptedPassword);
    alert(`Recovered password: ${decryptedPassword}`);
  } else {
    alert("Failed to recover account.");
  }
}
</script>

<template>
  <div class="recovery-container">
    <div class="title">
      <h1 class="title">Recovery</h1>
    </div>
    <div class="content">
      <p>
        Enter your <span class="has-text-primary">username</span> and
        <span class="has-text-primary">secret</span> to recover your account.
      </p>
      <div class="form">
        <div class="field">
          <label class="label">Username</label>
          <div class="control">
            <input
              class="input"
              type="text"
              placeholder="Username"
              v-model="username"
            />
          </div>
        </div>
        <div class="field">
          <label class="label">Secret</label>
          <div class="control">
            <input
              class="input"
              type="password"
              placeholder="Secret"
              v-model="secret"
            />
          </div>
        </div>
        <div class="field">
          <button
            v-if="!username || !secret"
            class="button is-primary is-fullwidth"
            disabled
          >
            Recover
          </button>
          <button
            v-else
            class="button is-primary is-fullwidth"
            @click="recover"
          >
            Recover
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recovery-container {
  display: flex;
  flex-direction: column;
  align-items: start;
  width: 100vw;
  height: 100%;
  overflow: hidden;
  padding: 0 25%;
}

.title {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding-top: 2rem;
  font-size: 3rem;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 1rem 0;
  font-size: 1.5rem;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  padding: 1rem 0;
}

.field {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 1rem 0;
}
</style>
