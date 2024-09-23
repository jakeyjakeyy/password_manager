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
  <!-- <button @click="setSelectionHandler">Set Selection</button> -->
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

<style scoped></style>
