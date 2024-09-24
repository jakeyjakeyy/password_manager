<script setup lang="ts">
import { onMounted } from "vue";
import VaultEntryListItem from "./VaultEntryListItem.vue";
const { vaultEntries, selectedEntry } = defineProps([
  "vaultEntries",
  "selectedEntry",
]);
const emit = defineEmits(["updateEntries", "setSelection"]);
let active = false;

const setSelectionHandler = (entry: any) => {
  emit("setSelection", entry);
};
</script>

<template>
  <div class="vault-entry-list">
    <div v-for="entry in vaultEntries" :key="entry.id">
      <VaultEntryListItem
        v-if="entry !== selectedEntry"
        :entry="entry"
        @click="setSelectionHandler(entry)"
        :selectedEntry="selectedEntry"
      />
      <VaultEntryListItem
        v-else
        :entry="entry"
        @click="setSelectionHandler(null)"
        :selectedEntry="selectedEntry"
        :active="true"
      />
    </div>
  </div>
</template>

<style scoped>
.vault-entry-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  width: 100%;
  max-height: 70vh;
  overflow-y: auto;
  transition: all 0.3s;
}
</style>
