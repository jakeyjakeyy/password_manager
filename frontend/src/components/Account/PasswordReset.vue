<script setup lang="ts">
import { ref } from "vue";
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

async function resetPassword() {
  console.log("Resetting password...");
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
          class="button is-primary is-fullwidth"
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
