<script setup lang="ts">
import { defineComponent, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";
import {
  deriveKey,
  storeKey,
  deleteKey,
  generateRecoverySecret,
  encryptPassword,
  decryptPassword,
} from "@/utils/Cryptography";
import Qrcode from "qrcode.vue";
import * as account from "@/utils/Account";
const { cta } = defineProps(["cta"]);
const { cookies } = useCookies();
const serverURL = import.meta.env.VITE_BACKEND_URL;
const router = useRouter();

const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const twoFA = ref("");
const loggedin = ref(false);
const register = ref(false);
const value = ref("");
const secret = ref("");
const recovery = ref("");
const recoveryUrl = ref("");
const salt = ref("");
const toggleRecovery = ref(false);
const recoveryLoading = ref(false);

if (cookies.get("access_token") && cookies.get("refresh_token")) {
  loggedin.value = true;
}

if (!cta) {
  const checklogin = setInterval(() => {
    if (cookies.get("access_token") && cookies.get("refresh_token")) {
      loggedin.value = true;
    }
  }, 100);
  const checklogout = setInterval(() => {
    if (!cookies.get("access_token") && !cookies.get("refresh_token")) {
      loggedin.value = false;
    }
  }, 100);
}

function openModal($el: any) {
  $el.classList.add("is-active");
}
function closeModal($el: any) {
  let modal = document.getElementById("login-modal");
  if (cta) modal = document.getElementById("cta-modal");
  modal?.classList.remove("is-active");
}
function closeAllModals() {
  (document.querySelectorAll(".modal") || []).forEach(($modal) => {
    closeModal($modal);
  });
}

async function submitForm() {
  if (register.value && password.value !== confirmPassword.value) {
    alert("Passwords do not match");
    password.value = "";
    confirmPassword.value = "";
    return;
  } else if (register.value) {
    await handleRegister();
  } else {
    await handleLogin();
    closeAllModals();
    router.push("/vault");
  }
}

async function handleLogin() {
  register.value = false;
  const response = await fetch(`${serverURL}/api/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
      twoFA: twoFA.value,
    }),
  });

  const data = await response.json();
  if (data.detail || data.non_field_errors) {
    alert(data.detail ? data.detail : data.non_field_errors);
    username.value = "";
    password.value = "";
    twoFA.value = "";
    return;
  }
  cookies.set("refresh_token", data.refresh);
  cookies.set("access_token", data.access);

  // Get our salt
  salt.value = await account.getSalt();
  // Derive our key
  const key = await deriveKey(password.value, salt.value);
  await storeKey(key);

  localStorage.setItem("username", username.value);
  loggedin.value = true;
  username.value = "";
  password.value = "";
  confirmPassword.value = "";

  // Event listener to delete the derived key and trigger logout when the user leaves the page
  window.addEventListener("beforeunload", async (event) => {
    await handleLogout();
  });
}

async function handleRegister() {
  const response = await fetch(`${serverURL}/api/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  });
  const data = await response.json();
  if (data.error) {
    alert(data.error);
    return;
  }
  localStorage.setItem("username", username.value);
  value.value = data.uri;
  secret.value = extractSecret();
  salt.value = data.salt;
  // We don't automatically log in anymore because the user needs to register their 2FA first
  // register.value = false;
  // handleLogin();
}

const handleLogout = async () => {
  await account.handleLogout();
  loggedin.value = false;
  closeAllModals();
  router.push("/");
};

const closeQR = () => {
  value.value = "";
  register.value = false;
  password.value = "";
  confirmPassword.value = "";
};

async function confirmQR() {
  const res = await fetch(`${serverURL}/api/confirm2fa`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user: username.value,
    }),
  });
  // Generate recovery secret, triggering next step
  recovery.value = generateRecoverySecret();
  const blob = new Blob([recovery.value], { type: "text/plain" });
  recoveryUrl.value = URL.createObjectURL(blob);
  // closeQR();
}

async function confirmRecovery() {
  recoveryLoading.value = true;
  // function to call the recovery API
  await account.confirmRecovery(recovery.value, password.value, salt.value);
  recoveryLoading.value = false;
  closeQR();
}

function extractSecret() {
  const uri = value.value;
  const secret = uri.split("secret=")[1].split("&")[0];
  return secret;
}

document.addEventListener("DOMContentLoaded", () => {
  // Add a click event on buttons to open a specific modal
  document.addEventListener("click", (event: any) => {
    const $trigger = event.target.closest(".js-modal-trigger");

    if ($trigger) {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);

      openModal($target);
    }
  });

  // Add a click event on various child elements to close the parent modal
  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllModals();
    }
  });
});
</script>

<template>
  <div :class="cta ? 'cta-container' : 'login-container'">
    <div class="cta-login-container" v-if="cta">
      <!-- If CTA -->
      <button
        class="button js-modal-trigger cta is-primary"
        data-target="cta-modal"
        @click="register = true"
        aria-label="Register for Free"
      >
        Register for Free
      </button>
      <button
        class="button js-modal-trigger cta is-info"
        data-target="cta-modal"
        @click="register = false"
        aria-label="Login"
      >
        Login
      </button>
    </div>
    <div v-else>
      <!-- If not logged in -->
      <div class="nav-button-container">
        <button
          v-if="loggedin === false"
          class="button js-modal-trigger gap"
          data-target="login-modal"
          @click="register = true"
        >
          Register
        </button>
        <button
          v-if="loggedin === false"
          class="button js-modal-trigger"
          data-target="login-modal"
          @click="register = false"
        >
          Login
        </button>
        <!-- If logged in -->
        <button v-else class="button" @click="handleLogout">Logout</button>
      </div>
    </div>
    <div :id="cta ? 'cta-modal' : 'login-modal'" class="modal">
      <div class="modal-background"></div>

      <div class="modal-content">
        <div v-if="!value" class="box">
          <h1 v-if="register === false" class="title">Login</h1>
          <h1 v-else class="title">Register</h1>
          <form @submit.prevent="submitForm">
            <div class="field">
              <label class="label">Username</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  placeholder="Username"
                  autofocus
                  v-model="username"
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <input
                  class="input"
                  type="password"
                  placeholder="Password"
                  v-model="password"
                />
              </div>
            </div>

            <div class="field" v-if="!register">
              <label class="label">2FA</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  placeholder="2FA"
                  v-model="twoFA"
                />
              </div>
            </div>

            <div class="field" v-if="register">
              <label class="label">Confirm Password</label>
              <div class="control">
                <input
                  class="input"
                  type="password"
                  placeholder="Confirm Password"
                  v-model="confirmPassword"
                />
              </div>
            </div>

            <div class="field">
              <div class="control">
                <div class="forgot-password">
                  <RouterLink to="/recovery">Forgot Password?</RouterLink>
                </div>
                <button class="button is-link is-fullwidth" type="submit">
                  {{ register ? "Register" : "Login" }}
                </button>
              </div>
            </div>
          </form>
        </div>
        <div v-else-if="!recovery" class="box" id="qr-code-box">
          <h1 class="title">
            Scan the QR code below with your authenticator app
          </h1>
          <div class="qrcode">
            <qrcode v-if="register && value" :value="value" />
            <p>Or manually enter the secret: {{ secret }}</p>
          </div>
          <button class="button is-link" @click="confirmQR">
            I have scanned the QR code
          </button>
        </div>
        <div v-else class="box">
          <div class="recovery-container">
            <h1 class="title">Recovery Secret</h1>
            <p>
              Please download the following recovery secret and store it in a
              safe place. This secret is the
              <span
                class="has-text-info"
                style="font-style: italic; font-weight: bold"
                >ONLY</span
              >
              way recover your account in case you lose access to your 2FA
              device or forget your password.
            </p>
            <a :href="recoveryUrl" download="vault-recovery-secret.txt">
              Download Recovery Secret
            </a>
            <button
              :class="['button', recoveryLoading ? 'is-skeleton' : 'is-link']"
              @click="confirmRecovery"
            >
              Close
            </button>
          </div>
        </div>
        <button
          class="modal-close is-large"
          aria-label="close"
          @click="closeModal(cta)"
        ></button>
      </div>
    </div>
  </div>
</template>

<style>
.login-container {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.modal-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

#qr-code-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nav-button-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.qrcode {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 1rem;
}

.cta-container {
  height: 100%;
  width: 100%;
}

.cta-login-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 2rem;
  animation: slide-in-right 1s forwards;
}

.cta {
  height: 100%;
  width: 100%;
  border-radius: 30px;
  font-size: 2rem;
}

@media (max-width: 768px) {
  .login-modal {
    margin-left: 1rem;
    gap: 0.5rem;
  }
  .cta-login-container {
    gap: 1rem;
    flex-direction: column;
  }
}

@keyframes slide-in-right {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.recovery-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>
