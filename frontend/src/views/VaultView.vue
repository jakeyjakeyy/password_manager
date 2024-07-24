<script setup lang="ts">
import { checkLogin } from "@/utils/RefreshToken";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { Retrieve } from "@/utils/VaultEntry";
import AddEntryModal from "@/components/Vault/AddEntryModal.vue";
import VaultEntry from "@/components/Vault/VaultEntry.vue";
import ImportEntries from "@/components/Vault/ImportEntries.vue";

const router = useRouter();
const vaultEntries = ref([]);

onMounted(async () => {
  if (!checkLogin()) {
    router.push("/");
  } else {
    vaultEntries.value = await Retrieve();
    console.log(vaultEntries.value);
  }
});
</script>

<template>
  <div class="vaultContainer">
    <div class="vaultHeader">
      <h1 class="title">Vault</h1>
      <div class="vaultHeaderButtons">
        <button class="button js-modal-trigger" data-target="add-entry-modal">
          Add Entry
        </button>
        <button class="button js-modal-trigger" data-target="import-modal">
          Import
        </button>
      </div>
    </div>
    <AddEntryModal />
    <ImportEntries />
    <div v-if="!vaultEntries.length" class="vaultEntries">
      <p>No entries found</p>
    </div>
    <div v-else class="vaultEntries">
      <div v-for="entry in vaultEntries" class="vaultEntry">
        <VaultEntry :entry="entry" />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
