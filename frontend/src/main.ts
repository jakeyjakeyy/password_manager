import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import { OhVueIcon, addIcons } from "oh-vue-icons";
import {
  BiEye,
  BiEyeSlash,
  BiClipboardCheck,
  BiClipboard,
} from "oh-vue-icons/icons";

addIcons(BiEye, BiEyeSlash, BiClipboardCheck, BiClipboard);

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.component("v-icon", OhVueIcon);

app.mount("#app");
