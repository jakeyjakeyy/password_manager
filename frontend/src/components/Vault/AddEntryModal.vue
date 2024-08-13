<script setup lang="ts">
import { ref } from "vue";
import { Add, Retrieve } from "@/utils/VaultEntry";
const { updateEntries } = defineProps(["updateEntries"]);
const username = ref("");
const password = ref("");
const name = ref("");
const hidden = ref(true);

const handleClick = async () => {
  const add = await Add(password.value, username.value, name.value);
  updateEntries();
  const modal = document.getElementById("add-entry-modal");
  if (modal) modal.classList.remove("is-active");
};

const length = ref(20);
const numbers = ref(true);
const symbols = ref(true);
const uppercase = ref(true);
const lowercase = ref(true);

const generatePassword = () => {
  const charset = [];
  if (numbers.value) charset.push("0123456789");
  if (symbols.value) charset.push("!@#$%^&*()_+-=[]{}|;:,.<>/?");
  if (uppercase.value) charset.push("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
  if (lowercase.value) charset.push("abcdefghijklmnopqrstuvwxyz");
  password.value = "";
  for (let i = 0; i < length.value; i++) {
    const index = Math.floor(Math.random() * charset.length);
    const charIndex = Math.floor(Math.random() * charset[index].length);
    password.value += charset[index][charIndex];
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
          <button class="button" @click="hidden = !hidden">
            {{ hidden ? "Show" : "Hide" }}
          </button>
          <button class="button" @click="generatePassword">Generate</button>
          <div class="control">
            <div class="generateOptions">
              <div class="lengthContainer">
                <input type="range" v-model="length" min="8" max="64" />
                <label>{{ length }}</label>
              </div>
              <div class="checkboxContainer">
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
            <input
              v-model="password"
              class="input"
              :type="hidden ? 'password' : 'text'"
              placeholder="Password"
            />
          </div>
        </div>
        <button class="button is-primary is-fullwidth" @click="handleClick">
          Add
        </button>
      </div>
    </div>
  </div>
</template>
