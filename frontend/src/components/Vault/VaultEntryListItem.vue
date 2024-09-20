<script setup lang="ts">
import { onMounted } from "vue";

const { entry, selectedEntry } = defineProps(["entry", "selectedEntry"]);
let active = false;

onMounted(() => {
  console.log(selectedEntry);
  if (selectedEntry && entry.id === selectedEntry.id) {
    active = true;
  }
});
</script>

<template>
  <div class="vault-entry-list-item border">
    {{ entry.name }}
  </div>
</template>

<style scoped>
.vault-entry-list-item {
  display: flex;
  justify-content: center;
  padding: 1rem;
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  cursor: pointer;
}

.border {
  border-image: linear-gradient(to right, #3acfd5 0%, #3a4ed5 100%) 1;
  border-width: 1px;
  border-style: solid;
  padding: 5px;
}
</style>
