<script setup lang="ts">
import VaultEntryListItem from "./VaultEntryListItem.vue";
const { vaultEntries } = defineProps(["vaultEntries"]);
const emit = defineEmits(["updateEntries", "setSelection"]);

const setSelectionHandler = (entry: any) => {
  emit("setSelection", entry);
};
</script>

<template>
  <!-- <button @click="setSelectionHandler">Set Selection</button> -->
  <div class="vault-entry-list">
    <div v-for="entry in vaultEntries" :key="entry.id">
      <VaultEntryListItem :entry="entry" @click="setSelectionHandler(entry)" />
    </div>
  </div>
</template>

<style scoped></style>
