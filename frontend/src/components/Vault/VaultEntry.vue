<script setup lang="ts">
import { onMounted, ref } from "vue";
import { decryptPassword } from "@/utils/Cryptography";
const { entry } = defineProps(["entry"]);
const showPassword = ref(false);
const password = ref("");
const copiedConfirmation = ref(false);

onMounted(async () => {
  password.value = await decryptPassword(entry.password, entry.iv);
});

const copyPassword = () => {
  navigator.clipboard.writeText(password.value);

  copiedConfirmation.value = true;
  setTimeout(() => {
    copiedConfirmation.value = false;
  }, 1000);
};
</script>

<template>
  <div class="vaultEntry">
    <div class="vaultEntryHeader">
      <h1 class="title">{{ entry.name }}</h1>
    </div>
    <div class="vaultEntryUsername">
      <p>{{ entry.username }}</p>
    </div>
    <div class="vaultEntryPassword">
      <button class="button is-primary" @click="showPassword = !showPassword">
        {{ showPassword ? "Hide Password" : "Show Password" }}
      </button>
      <button
        v-if="!copiedConfirmation"
        class="button is-primary"
        @click="copyPassword"
      >
        Copy Password
      </button>
      <button v-else class="button is-success">Copied!</button>
      <p v-if="showPassword">{{ password }}</p>
      <p v-else>
        <span v-for="i in password.length">*</span>
      </p>
    </div>
  </div>
</template>

<style scoped></style>
