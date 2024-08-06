<script setup lang="ts">
import { checkLogin } from "@/utils/RefreshToken";
import { useRouter } from "vue-router";
import { ref, onMounted, watch } from "vue";
import { Retrieve } from "@/utils/VaultEntry";
import Fuse from "fuse.js";
import AddEntryModal from "@/components/Vault/AddEntryModal.vue";
import VaultEntry from "@/components/Vault/VaultEntry.vue";
import ImportEntries from "@/components/Vault/ImportEntries.vue";

interface VaultEntry {
  id: number;
  name: string;
  username: string;
  password: string;
  iv: string;
}

const fuseOptions = {
  keys: ["name", "username", "url", "notes"],
  includeScore: true,
  includeMatches: true,
  threshold: 0.3,
  minMatchCharLength: 1,
};

const router = useRouter();
const vaultEntries = ref([]);
const searchTerm = ref("");
const searchList = ref([]);
const sortBy = ref("name");
let fuse: any;

onMounted(async () => {
  if (!checkLogin()) {
    router.push("/");
  } else {
    vaultEntries.value = await Retrieve();
    fuse = new Fuse(vaultEntries.value, fuseOptions);
  }
});

const handleSearch = () => {
  searchList.value = fuse
    .search(searchTerm.value)
    .map((result: any) => result.item);
};

const handleSort = () => {
  if (sortBy.value === "name") {
    vaultEntries.value.sort((a: VaultEntry, b: VaultEntry) => {
      if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
      if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
      return 0;
    });
  } else if (sortBy.value === "newest") {
    vaultEntries.value.sort((a: VaultEntry, b: VaultEntry) => {
      if (a.id < b.id) return 1;
      if (a.id > b.id) return -1;
      return 0;
    });
  }
};

const updateEntries = async () => {
  vaultEntries.value = await Retrieve();
  fuse = new Fuse(vaultEntries.value, fuseOptions);
};
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
      <div class="select">
        <select v-model="sortBy" @change="handleSort">
          <option value="name">Name</option>
          <option value="newest">Newest</option>
        </select>
      </div>
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Search"
        class="input"
        @input="handleSearch"
      />
    </div>
    <AddEntryModal :updateEntries="updateEntries" />
    <ImportEntries />
    <div v-if="!vaultEntries.length" class="vaultEntries">
      <p>No entries found</p>
    </div>
    <div v-else-if="searchList.length" class="vaultEntries">
      <div v-for="entry in searchList" class="vaultEntry">
        <VaultEntry :entry="entry" />
      </div>
    </div>
    <div v-else class="vaultEntries">
      <div v-for="entry in vaultEntries" class="vaultEntry">
        <VaultEntry :entry="entry" :updateEntries="updateEntries" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.vaultContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 90vh;
  max-width: 100vw;
}

.vaultEntries {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
</style>
