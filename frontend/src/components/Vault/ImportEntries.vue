<script setup lang="ts">
import { ref } from "vue";
import { AddBatch } from "@/utils/VaultEntry";
const entries = ref<File | null>(null);
const fileContent = ref<any>(null);
import { encryptPassword } from "@/utils/Cryptography";

const handleClick = () => {
  // Default handling based on KeeperSecurity JSON export format
  Import();
};

const handleFileChange = (e: Event) => {
  // Set entries to the file that the user uploads
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length) {
    entries.value = target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        fileContent.value = JSON.parse(e.target?.result as string);
      } catch (err) {
        console.error(err);
        fileContent.value = null;
      }
    };
    reader.readAsText(target.files[0]);
  } else {
    entries.value = null;
    fileContent.value = null;
  }
};

async function Import() {
  let entriesDict = <any>[];
  let i = 0;
  for (const entry of fileContent.value["records"]) {
    entriesDict[i] = {};
    entriesDict[i].name = entry.title;
    let encrypted = await encryptPassword(entry.password);
    entriesDict[i].password = encrypted.encryptedPassword;
    entriesDict[i].iv = encrypted.iv;
    if (entry.login) {
      entriesDict[i].username = entry.login;
    } else {
      entriesDict[i].username = "";
    }
    i++;
  }
  const response = await AddBatch(entriesDict);
}
</script>

<template>
  <div id="import-modal" class="modal">
    <div class="modal-background"></div>
    <div class="modal-content">
      <div class="box">
        <h1 class="title">Import Entries</h1>
        <div class="field">
          <label class="label">Entries</label>
          <div class="control">
            <div class="file has-name is-fullwidth">
              <label class="file-label">
                <input
                  class="file-input"
                  type="file"
                  name="entries"
                  @change="handleFileChange"
                />
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label"> Choose a file… </span>
                </span>
                <span class="file-name">{{
                  entries ? entries.name : "No File Chosen"
                }}</span>
              </label>
            </div>
          </div>
        </div>
        <button class="button is-primary is-fullwidth" @click="handleClick">
          Import
        </button>
      </div>
    </div>
  </div>
</template>
