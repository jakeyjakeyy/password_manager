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
const copiedValue = ref<null | string>(null);
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
  input.accept = ".txt,.csv,.json,.pdf,.zip";
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

function handleCopy(value: string, type: string) {
  navigator.clipboard.writeText(value);
  copiedValue.value = type;
  copiedConfirmation.value = true;
  setTimeout(() => {
    copiedConfirmation.value = false;
  }, 1000);
}
</script>

<template>
  <div class="vaultEntry">
    <div class="vault-entry-content-container">
      <div class="vaultEntryHeader">
        <!-- Entry Name -->
        <h1 class="title">Entry Name</h1>
        <p
          v-if="!editing"
          class="subtitle"
          @click="handleCopy(entry.name, 'name')"
        >
          {{ entry.name }}
          <span v-if="copiedValue === 'name' && copiedConfirmation">
            Copied!
          </span>
        </p>
        <input
          v-else
          class="input"
          type="text"
          v-model="entry.name"
          :placeholder="entry.name"
          v-on:change="changedValues = true"
        />
      </div>
      <!-- Entry Username -->
      <div class="vaultEntryUsername">
        <h1 class="title">Username</h1>
        <p
          v-if="!editing"
          class="subtitle"
          @click="handleCopy(entry.username, 'username')"
        >
          {{ entry.username }}
          <span v-if="copiedValue === 'username' && copiedConfirmation">
            Copied!
          </span>
        </p>
        <input
          v-else
          class="input"
          type="text"
          v-model="entry.username"
          :placeholder="entry.username"
          v-on:change="changedValues = true"
        />
      </div>
      <!-- Entry Password -->
      <div class="vaultEntryPassword">
        <h1 class="title">Password</h1>
        <!-- Password Controls -->
        <div class="password-controls">
          <button
            class="button is-primary is-fullwidth"
            @click="handleShowPassword"
          >
            <v-icon v-if="showPassword" name="bi-eye-slash" scale="1.25" />
            <v-icon v-else name="bi-eye" scale="1.25" />
          </button>
        </div>
        <p v-if="showPassword && !editing" class="subtitle">{{ password }}</p>
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
        <p v-else @click="handleCopy(password, 'password')" class="subtitle">
          <span v-for="i in password.length">*</span>
          <span v-if="copiedValue === 'password' && copiedConfirmation">
            Copied!
          </span>
        </p>
      </div>
      <!-- Entry Files -->
      <div class="vaultEntryFiles">
        <h1 class="title">Files</h1>
        <button class="button is-link" @click="uploadFile" id="add-files">
          Add Files
        </button>
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
        id="save-button"
        disabled
        @click="submitEdit"
      >
        Save Changes
      </button>
      <button
        v-if="editing && changedValues"
        class="button is-primary"
        id="save-button"
        @click="submitEdit"
      >
        Save Changes
      </button>
      <button
        class="button is-danger js-modal-trigger"
        id="delete-button"
        :data-target="'confirm-delete-entry-modal' + entry.id"
      >
        Delete
      </button>
    </div>
    <div class="entry-button-controls">
      <!-- Close Editing Button -->
      <button v-if="!editing" class="button" @click="handleEdit">
        <v-icon name="bi-pencil-square" scale="1.25" />
      </button>
      <button v-else class="button" @click="editing = false">
        <v-icon name="bi-check-lg" scale="1.25" />
      </button>
      <!-- Deselect Button -->
      <button
        class="deselect-button button"
        aria-label="close"
        @click="emitUnselect()"
      >
        <v-icon name="io-close-sharp" scale="1.25" />
      </button>
    </div>
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
  gap: 1rem;
}
.vaultEntryHeader {
  display: flex;
  flex-direction: column;
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
  width: fit-content;
}

.vault-entry-content-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entry-button-controls {
  display: flex;
  flex-direction: row;
  position: absolute;
  top: 0;
  right: 0;
  margin: 1rem;
  gap: 0.5rem;
}

.password-controls {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  margin-left: 1rem;
}

.subtitle {
  margin-top: 0.5rem;
  margin-left: 1rem;
}

@media (max-width: 768px) {
  .vaultEntry {
    margin-top: 0;
    padding-top: 0.5rem;
    border-top: 1px solid var(--bulma-primary);
  }

  .password-controls {
    width: 100%;
    padding-right: 1rem;
  }

  .vaultEntryHeader,
  .vaultEntryUsername,
  .vaultEntryPassword {
    width: 100%;
    padding-right: 1rem;
  }

  .vault-entry-post-controller {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
  }

  #delete-button {
    width: 30%;
  }

  #save-button {
    flex: 1;
  }

  #add-files {
    width: 100%;
  }
}
</style>
