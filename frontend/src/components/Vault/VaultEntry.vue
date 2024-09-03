<script setup lang="ts">
import { onMounted, ref } from "vue";
import { decryptPassword } from "@/utils/Cryptography";
import { Edit, Delete, Retrieve } from "@/utils/VaultEntry";
import { checkToken } from "@/utils/RefreshToken";
const { entry, updateEntries } = defineProps(["entry", "updateEntries"]);
const serverURL = import.meta.env.VITE_BACKEND_URL;
const showPassword = ref(false);
const password = ref("");
const copiedConfirmation = ref(false);
const modal = ref<HTMLElement | null>(null);
const editing = ref(false);
const changedValues = ref(false);
let showPasswordTimeout: any = null;

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
  if (showPassword.value) {
    if (showPasswordTimeout) clearTimeout(showPasswordTimeout);
    showPasswordTimeout = setTimeout(() => {
      showPassword.value = false;
    }, 5000);
  }
};

const handleEdit = () => {
  if (!checkToken()) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
  }
  editing.value = true;
  changedValues.value = false;
};

const submitEdit = async () => {
  if (!changedValues.value) {
    editing.value = false;
    return;
  }
  const response = await Edit(
    entry.id,
    password.value,
    entry.username,
    entry.name
  );
  editing.value = false;
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

function closeModal() {
  if (modal.value) modal.value.classList.remove("is-active");
}
</script>

<template>
  <div class="vaultEntry">
    <div class="vaultEntryHeader">
      <h1 v-if="!editing" class="title">{{ entry.name }}</h1>
      <input
        v-else
        class="input"
        type="text"
        v-model="entry.name"
        :placeholder="entry.name"
        v-on:change="changedValues = true"
      />
      <button
        class="delete button js-modal-trigger"
        :data-target="'confirm-delete-entry-modal' + entry.id"
      ></button>
      <button v-if="!editing" class="button is-primary" @click="handleEdit">
        Edit
      </button>
      <button v-else class="button is-primary" @click="submitEdit">Save</button>
    </div>
    <div class="vaultEntryUsername">
      <p v-if="!editing">{{ entry.username }}</p>
      <p v-else>
        <input
          class="input"
          type="text"
          v-model="entry.username"
          :placeholder="entry.username"
          v-on:change="changedValues = true"
        />
      </p>
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
      <p v-if="showPassword && !editing">{{ password }}</p>
      <input
        v-else-if="!showPassword && editing"
        class="input"
        type="password"
        v-model="password"
        :placeholder="password"
        v-on:change="changedValues = true"
      />
      <input
        v-else-if="showPassword && editing"
        class="input"
        type="text"
        v-model="password"
        :placeholder="password"
        v-on:change="changedValues = true"
      />
      <p v-else>
        <span v-for="i in password.length">*</span>
      </p>
    </div>
    <div class="vaultEntryFiles">
      <button class="button is-primary">Files</button>
    </div>
    <div
      class="modal"
      :id="'confirm-delete-entry-modal' + entry.id"
      ref="modal"
    >
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">
          <p>Are you sure you want to delete this entry?</p>
          <button class="button is-danger" @click="handleDelete">Delete</button>
          <button class="button" @click="closeModal()">Cancel</button>
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
