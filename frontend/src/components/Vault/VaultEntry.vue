<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import {
  decryptPassword,
  decryptFile,
  encryptFile,
} from "@/utils/Cryptography";
import { Edit, Delete, AddFile, DeleteFile } from "@/utils/VaultEntry";
import { checkToken } from "@/utils/RefreshToken";
const emit = defineEmits(["unselect"]);
const { entry, updateEntries } = defineProps(["entry", "updateEntries"]);
const showPassword = ref(false);
const password = ref("");
const copiedConfirmation = ref(false);
const modal = ref<HTMLElement | null>(null);
const editing = ref(false);
const changedValues = ref(false);
const files = ref<{ file: File; url: string; id: number }[]>([]);
let showPasswordTimeout: any = null;

onMounted(async () => {
  password.value = await decryptPassword(entry.password, entry.iv);
  for (const file of entry.files) {
    const decryptedFile = await decryptFile(file.file, file.iv, file.name);
    const url = URL.createObjectURL(decryptedFile);
    let fileObj = { file: decryptedFile, url: url, id: file.id };
    files.value.push(fileObj);
  }
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
  if (!response.error) {
    if (response.code === "token_not_valid") {
      alert("Session expired. Please log in again.");
      window.location.href = "/";
    }
    updateEntries();
    closeModal();
    emitUnselect();
  } else {
    alert("Failed to delete entry");
  }
};

function closeModal() {
  if (modal.value) modal.value.classList.remove("is-active");
}

const uploadFile = async () => {
  const input = document.createElement("input");
  input.type = "file";
  input.onchange = async (e: any) => {
    const file = e.target.files[0];
    const encryptedFile = await encryptFile(file);
    const res = await AddFile(
      encryptedFile.encryptedFile,
      encryptedFile.iv,
      file.name,
      entry.id
    );
    if (res.error) {
      alert(res.message);
      return;
    }
    const decryptedFile = await decryptFile(
      encryptedFile.encryptedFile,
      encryptedFile.iv,
      file.name
    );
    const url = URL.createObjectURL(decryptedFile);
    let fileObj = { file: decryptedFile, url: url, id: res.id };
    files.value.push(fileObj);
  };
  input.click();
};

const handleDeleteFile = async (id: number) => {
  const response = await DeleteFile(id);
  if (response) {
    files.value = files.value.filter((file) => file.id !== id);
  } else {
    alert("Failed to delete file");
  }
};

function emitUnselect() {
  emit("unselect");
}
</script>

<template>
  <div class="vaultEntry">
    <div class="vault-entry-content-container">
      <div class="vaultEntryHeader">
        <h1 v-if="!editing" class="title" @click="handleEdit">
          {{ entry.name }}
        </h1>
        <input
          v-else
          class="input"
          type="text"
          v-model="entry.name"
          :placeholder="entry.name"
          v-on:change="changedValues = true"
        />
      </div>
      <div class="vaultEntryUsername">
        <p v-if="!editing" @click="handleEdit">{{ entry.username }}</p>
        <input
          v-else
          class="input"
          type="text"
          v-model="entry.username"
          :placeholder="entry.username"
          v-on:change="changedValues = true"
        />
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
        <p v-else @click="handleEdit">
          <span v-for="i in password.length">*</span>
        </p>
      </div>
      <div class="vaultEntryFiles">
        <button class="button is-primary" @click="uploadFile">Add Files</button>
        <div v-for="file in files" class="vaultEntryFile">
          <p>{{ file.file.name }}</p>
          <div class="buttons are-small">
            <button class="button is-danger" @click="handleDeleteFile(file.id)">
              Delete
            </button>
            <a :href="file.url" download>
              <button class="button is-primary">Download</button>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="vault-entry-post-controller">
      <button
        v-if="!editing || !changedValues"
        class="button is-primary"
        disabled
        @click="submitEdit"
      >
        Save Changes
      </button>
      <button
        v-if="editing && changedValues"
        class="button is-primary"
        @click="submitEdit"
      >
        Save Changes
      </button>
      <button
        class="button is-danger js-modal-trigger"
        :data-target="'confirm-delete-entry-modal' + entry.id"
      >
        Delete
      </button>
    </div>
    <!-- Deselect Button -->
    <button
      class="deselect-button button"
      aria-label="close"
      @click="emitUnselect()"
    >
      X
    </button>
    <!-- Modal -->
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
.vaultEntry {
  position: relative;
  margin-top: 5rem;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.vaultEntryHeader {
  display: flex;
  flex-direction: row;
}
.vaultEntryFile {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.vaultEntryHeader,
.vaultEntryUsername,
.vaultEntryPassword {
  cursor: pointer;
}

.vault-entry-post-controller {
  display: flex;
  flex-direction: row;
}

.deselect-button {
  position: absolute;
  top: 0;
  right: 0;
  margin: 1rem;
}
</style>
