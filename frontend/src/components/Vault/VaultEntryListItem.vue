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
  <div v-else class="vault-entry-list-item border">
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
  border-image: linear-gradient(to right, #3acfd5 0%, #3a4ed5 100%) 1;
  border-width: 1px;
  border-style: solid;
  padding: 5px;
}

.active {
  animation: turnActive 0.5s forwards;
  background-color: linear-gradient(to right, #3acfd5 0%, #3a4ed5 100%);
}

@keyframes turnActive {
  100% {
    background-color: #3acfd5;
    color: white;
  }
}
</style>
