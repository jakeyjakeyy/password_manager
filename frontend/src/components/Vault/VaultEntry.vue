<script setup lang="ts">
import { onMounted, ref } from "vue";
import { decryptPassword } from "@/utils/Cryptography";
import { Edit, Delete, Retrieve } from "@/utils/VaultEntry";
const { entry, updateEntries } = defineProps(["entry", "updateEntries"]);
const serverURL = import.meta.env.VITE_BACKEND_URL;
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

const handleShowPassword = () => {
  showPassword.value = !showPassword.value;
  setTimeout(() => {
    showPassword.value = false;
  }, 5000);
};

const handleEdit = async () => {
  const response = await fetch(`${serverURL}/api/vault/edit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(entry),
  });
};

const handleDelete = async () => {
  const response = await Delete(entry.id);
  console.log(response);
  if (response) {
    console.log("Deleted entry");
    updateEntries();
  } else {
    alert("Failed to delete entry");
  }
};
</script>

<template>
  <div class="vaultEntry">
    <div class="vaultEntryHeader">
      <h1 class="title">{{ entry.name }}</h1>
      <button
        class="delete button js-modal-trigger"
        data-target="confirm-delete-entry-modal"
      ></button>
      <button class="button is-primary" @click="handleEdit">Edit</button>
    </div>
    <div class="vaultEntryUsername">
      <p>{{ entry.username }}</p>
    </div>
    <div class="vaultEntryPassword">
      <button class="button is-primary" @click="handleShowPassword">
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
    <div class="modal" id="confirm-delete-entry-modal">
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">
          <p>Are you sure you want to delete this entry?</p>
          <button class="button is-danger" @click="handleDelete">Delete</button>
          <button class="button">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vaultEntryHeader {
  display: flex;
  flex-direction: row;
}
</style>
