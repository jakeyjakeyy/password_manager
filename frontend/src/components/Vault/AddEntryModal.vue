<script setup lang="ts">
import { ref } from "vue";
import { Add } from "@/utils/VaultEntry";
const username = ref("");
const password = ref("");
const name = ref("");
const hidden = ref(true);

const handleClick = () => {
  Add(password.value, username.value, name.value);
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
          <div class="control">
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
