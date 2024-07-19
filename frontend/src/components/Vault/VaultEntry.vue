<script setup lang="ts">
import { onMounted, ref } from "vue";
import { decryptPassword } from "@/utils/Cryptography";
const { entry } = defineProps(["entry"]);
const showPassword = ref(false);
const password = ref("");

onMounted(async () => {
  password.value = await decryptPassword(entry.password, entry.iv);
});
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
      <p v-if="showPassword">{{ password }}</p>
      <p v-else>
        <span v-for="i in password.length">*</span>
      </p>
    </div>
  </div>
</template>

<style scoped></style>
