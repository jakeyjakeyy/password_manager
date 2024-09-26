<script setup lang="ts">
import { onMounted, watch } from "vue";

const props = defineProps(["entry", "selectedEntry", "active"]);
</script>

<template>
  <div
    v-if="entry === selectedEntry"
    class="vault-entry-list-item border active"
  >
    {{ entry.name }}
  </div>
  <div v-else class="vault-entry-list-item border inactive">
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
  transition: all 0.3s;
}

.border {
  border-image: linear-gradient(
      to right,
      var(--primary) 0%,
      var(--secondary) 100%
    )
    1;
  border-width: 1px;
  border-style: solid;
  padding: 5px;
}

.active {
  animation: turnActive 0.5s forwards;
}

@keyframes turnActive {
  100% {
    background-color: var(--accent);
    color: white;
  }
}

.inactive {
  animation: turnInactive 0.5s forwards;
}

@keyframes turnInactive {
  0% {
    background-color: var(--accent);
    color: white;
  }
  100% {
    background-color: var(--bulma-background-color);
  }
}
</style>
