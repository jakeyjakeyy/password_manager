<script setup lang="ts">
import { ref } from "vue";
import { Add, AddFile } from "@/utils/VaultEntry";
import { encryptFile, decryptFile } from "@/utils/Cryptography";
const { updateEntries } = defineProps(["updateEntries"]);
const username = ref("");
const password = ref("");
const name = ref("");
const hidden = ref(true);
const files = ref<File[]>([]);

const handleClick = async () => {
  const add = await Add(password.value, username.value, name.value);
  if (add) {
    for (const file of files.value) {
      const encryptedFile = await encryptFile(file);
      await AddFile(
        encryptedFile.encryptedFile,
        encryptedFile.iv,
        file.name,
        add.id
      );
    }
  }
  clearVars();
  updateEntries();
  closeModal();
};

function closeModal() {
  clearVars();
  const modal = document.getElementById("add-entry-modal");
  if (modal) modal.classList.remove("is-active");
}

function clearVars() {
  username.value = "";
  password.value = "";
  name.value = "";
  files.value = [];
}

const length = ref(20);
const numbers = ref(true);
const symbols = ref(true);
const uppercase = ref(true);
const lowercase = ref(true);

const generatePassword = () => {
  const charset = new Uint32Array(length.value);
  self.crypto.getRandomValues(charset);
  let charsetChars = "";
  if (numbers.value) charsetChars += "0123456789";
  if (symbols.value) charsetChars += "!@#$%^&*()_+";
  if (uppercase.value) charsetChars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  if (lowercase.value) charsetChars += "abcdefghijklmnopqrstuvwxyz";
  let pwd = "";
  for (let i = 0; i < length.value; i++) {
    pwd += charsetChars.charAt(charset[i] % charsetChars.length);
  }
  password.value = pwd;
};

const onFileChange = async (e: any) => {
  const file = e.target.files[0];
  if (file.size > 5 * 1024 * 1024) {
    alert("File size must be less than 5MB");
    return;
  }
  files.value.push(file);
};

const removeFile = (file: File) => {
  const index = files.value.indexOf(file);
  if (index > -1) {
    files.value.splice(index, 1);
  }
};
</script>

<template>
  <div id="add-entry-modal" class="modal">
    <div class="modal-background"></div>
    <div class="modal-content">
      <div class="box">
        <h1 class="title">Add Entry</h1>
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input
              v-model="name"
              class="input"
              type="text"
              placeholder="Name"
            />
          </div>
        </div>
        <div class="field">
          <label class="label">Username</label>
          <div class="control">
            <input
              v-model="username"
              class="input"
              type="text"
              placeholder="Username"
            />
          </div>
        </div>
        <div class="field">
          <label class="label">Password</label>
          <button
            class="button is-fullwidth is-info is-outlined"
            @click="generatePassword"
          >
            Generate
          </button>
          <div class="control">
            <div class="generate-options">
              <div class="length-container">
                <input type="range" v-model="length" min="8" max="64" />
                <label>{{ length }}</label>
              </div>
              <div class="checkbox-container">
                <label class="checkbox">
                  <input type="checkbox" v-model="numbers" />
                  Numbers
                </label>
                <label class="checkbox">
                  <input type="checkbox" v-model="symbols" />
                  Symbols
                </label>
                <label class="checkbox">
                  <input type="checkbox" v-model="uppercase" />
                  Uppercase
                </label>
                <label class="checkbox">
                  <input type="checkbox" v-model="lowercase" />
                  Lowercase
                </label>
              </div>
            </div>
            <div class="password-input">
              <input
                v-model="password"
                class="input"
                :type="hidden ? 'password' : 'text'"
                placeholder="Password"
              />
              <span>
                <button class="button" @click="hidden = !hidden">
                  {{ hidden ? "Show" : "Hide" }}
                </button></span
              >
            </div>
          </div>
          <div class="fileUpload">
            <label class="label">Files</label>
            <label class="file-label">
              <input
                class="file-input"
                type="file"
                accept=".txt,.csv,.json,.pdf,.zip"
                v-on:change="onFileChange"
              />
              <span class="file-cta">
                <span class="file-label">Choose a file…</span>
              </span>
            </label>
            <div v-for="file in files" class="file">
              <p>{{ file.name }}</p>
              <button class="button is-danger" @click="removeFile(file)">
                Delete
              </button>
            </div>
          </div>
        </div>
        <button class="button is-primary is-fullwidth" @click="handleClick">
          Add
        </button>
      </div>
      <span class="modal-close is-large" @click="closeModal"></span>
    </div>
  </div>
</template>

<style scoped>
.file {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.generate-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-container,
.length-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.password-input {
  display: flex;
  padding: 1rem 0;
}
</style>
