<script setup lang="ts">
import { checkToken } from "@/utils/RefreshToken";
import { useRouter } from "vue-router";
import { ref, onMounted, watch } from "vue";
import { Retrieve } from "@/utils/VaultEntry";
import Fuse from "fuse.js";
import AddEntryModal from "@/components/Vault/AddEntryModal.vue";
import VaultEntry from "@/components/Vault/VaultEntry.vue";
import ImportEntries from "@/components/Vault/ImportEntries.vue";
import VaultEntryList from "@/components/Vault/VaultEntryList.vue";

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
  if (!checkToken()) {
    // Redirect to login if token is invalid
    window.location.href = "/";
  } else {
    // Retrieve vault entries and initialize Fuse
    vaultEntries.value = await Retrieve();
    fuse = new Fuse(vaultEntries.value, fuseOptions);
    const navRouterButtons = document.querySelectorAll(".navbar-item");
    navRouterButtons.forEach((button) => {
      if (button.id === "vaultRouterButton") button.classList.add("is-active");
      else button.classList.remove("is-active");
    });
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

const setSelection = (event: any) => {
  console.log("setSelection", event);
};
</script>

<template>
  <div class="vaultContainer">
    <div class="vault-nav">
      <div class="vault-controller-container">
        <div class="vaultHeader">
          <div class="vaultHeaderButtons">
            <button
              class="button js-modal-trigger"
              data-target="add-entry-modal"
            >
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
      </div>
      <AddEntryModal :updateEntries="updateEntries" />
      <ImportEntries />
      <div class="vault-entries-container">
        <div v-if="!vaultEntries.length" class="vaultEntries">
          <p>No entries found</p>
        </div>
        <div v-else-if="searchList.length" class="vaultEntries">
          <div v-for="entry in searchList" class="vaultEntry">
            <VaultEntry :entry="entry" :updateEntries="updateEntries" />
          </div>
        </div>
        <div v-else class="vaultEntries">
          <VaultEntryList
            @set-selection="setSelection"
            :vaultEntries="vaultEntries"
          />
        </div>
      </div>
    </div>
    <div class="vault-browser">
      <p>hello</p>
    </div>
  </div>
</template>

<style scoped>
.vaultContainer {
  display: flex;
  flex-direction: row;
  align-items: start;
  height: 100%;
  width: 100vw;
}

.vault-nav {
  display: flex;
  flex-direction: column;
  width: 30%;
  height: 100%;
  padding: 1rem;
}

.vaultEntries {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
</style>
