<script setup lang="ts">
import { checkToken } from "@/utils/RefreshToken";
import { useRouter } from "vue-router";
import { ref, onMounted, watch, onUnmounted } from "vue";
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

const selectedEntry = ref<VaultEntry | null>(null);

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
    // initialize list sorting
    handleSort();
  }

  // Timer to check for token expiration
  setInterval(() => {
    if (!checkToken()) {
      // Redirect to login if token is invalid
      window.location.href = "/";
    }
  }, 60000);
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
  if (event) selectedEntry.value = event;
  else selectedEntry.value = null;
};
</script>

<template>
  <div class="vault-container">
    <div class="vault-nav">
      <div class="vault-controller-container">
        <div class="vault-header">
          <div class="vault-header-buttons">
            <button
              class="button js-modal-trigger add"
              data-target="add-entry-modal"
            >
              Add Entry
            </button>
            <button
              class="button js-modal-trigger import"
              data-target="import-modal"
            >
              Import
            </button>
          </div>
          <div class="vault-header-search">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Search"
              class="search-input input"
              @input="handleSearch"
            />
            <div class="select">
              <select v-model="sortBy" @change="handleSort" id="sortBy">
                <option value="name">Name</option>
                <option value="newest">Newest</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <AddEntryModal :updateEntries="updateEntries" />
      <ImportEntries @call-update-entries="updateEntries" />
      <div class="vault-entries-container">
        <div v-if="!vaultEntries.length" class="vault-entries">
          <p>No entries found</p>
        </div>
        <div v-else-if="searchList.length" class="vault-entries">
          <VaultEntryList
            @set-selection="setSelection"
            :vaultEntries="searchList"
            :selectedEntry="selectedEntry"
          />
        </div>
        <div v-else class="vault-entries">
          <VaultEntryList
            @set-selection="setSelection"
            :vaultEntries="vaultEntries"
            :selectedEntry="selectedEntry"
          />
        </div>
      </div>
    </div>
    <div v-if="selectedEntry" class="vault-browser">
      <VaultEntry
        :entry="selectedEntry"
        :updateEntries="updateEntries"
        @unselect="selectedEntry = null"
      />
    </div>
  </div>
</template>

<style scoped>
.vault-container {
  display: flex;
  flex-direction: row;
  align-items: start;
  width: 100vw;
  height: 100%;
  overflow: hidden;
}

.vault-nav {
  display: flex;
  flex-direction: column;
  width: 30vw;
  padding: 1rem;
}

.vault-entries-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
}

.vault-entries {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
}

.vault-browser {
  display: flex;
  flex-direction: column;
  width: 70vw;
  height: 100%;
  padding: 1rem;
}

.vault-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.vault-header-search,
.vault-header-buttons {
  display: flex;
  flex-direction: row;
}

.import,
.select {
  width: 20%;
}
.add,
.search-input {
  flex: 1;
}

#sortBy {
  width: 100%;
}

@media (max-width: 768px) {
  .vault-container {
    flex-direction: column;
  }
  .vault-nav {
    width: 100vw;
    height: 30vh;
    padding-bottom: 0;
  }
  .vault-browser {
    width: 100vw;
  }

  .import,
  .select {
    width: 35%;
  }
}
</style>
