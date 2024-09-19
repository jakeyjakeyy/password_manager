<script setup lang="ts">
const { entry } = defineProps(["entry"]);
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
}

.border {
  border-image: linear-gradient(to right, #3acfd5 0%, #3a4ed5 100%) 1;
  border-width: 1px;
  border-style: solid;
  padding: 5px;
}
</style>
