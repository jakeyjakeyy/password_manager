<script setup lang="ts">
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
import LoginModal from "@/components/LoginModal.vue";
import RefreshToken from "@/utils/RefreshToken";
const serverURL = import.meta.env.VITE_BACKEND_URL;
import * as Cryptography from "@/utils/Cryptography";
import * as VaultEntry from "@/utils/VaultEntry";
import Qrcode from "qrcode.vue";
import { ref } from "vue";

const value = ref(
  "otpauth://totp/Vault:user?secret=X4LDXPSDRPWDERMUL4CTWVULD3KLCIPM&issuer=Vault"
);

async function handleClick() {
  // const key = await Cryptography.retrieveKey();
  // const password = "test";
  // const encrypted = await Cryptography.encryptPassword(password, key);
  // console.log(encrypted);
  // const decrypted = await Cryptography.decryptPassword(
  //   encrypted.encryptedPassword,
  //   encrypted.iv,
  //   key
  // );
  // console.log(decrypted);
  VaultEntry.Add("testPassword2", "", "testName2");
  // const entry = await VaultEntry.Retrieve();
  // const decrypted = await Cryptography.decryptPassword(
  //   entry[0].password,
  //   entry[0].iv,
  //   await Cryptography.retrieveKey()
  // );
  // console.log(decrypted);
}
</script>

<template>
  <main>
    <h1>Home</h1>
    <LoginModal />
    <button class="button" @click="handleClick">Click me</button>
    <qrcode :value="value" />
  </main>
</template>
