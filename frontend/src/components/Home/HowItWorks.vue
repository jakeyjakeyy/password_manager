<script setup lang="ts"></script>

<template>
  <div class="how-it-works">
    <div class="header">
      <div class="header-title">
        <h1 class="title is-1">How It Works</h1>
      </div>
      <div class="header-content">
        <p class="subtitle is-4">
          Using guidelines approved for federal use by the
          <span
            ><a
              href="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-175Br1.pdf"
              class="bold"
              target="_blank"
              >National Institute of Standards and Technology (NIST)</a
            ></span
          >, The Vault ensure that your passwords and files remain secure and
          private.
        </p>
        <p class="subtitle is-4 has-text-info bold">
          Unencrypted/plaintext passwords and files are NEVER sent to, stored,
          or viewed by the servers.
          <br />
          All encryption, decryption, and key derivation is done locally for
          maximum security.
        </p>
      </div>
    </div>
    <div class="content">
      <div class="item">
        <div class="item-title">
          <h3 class="title is-3">Encryption</h3>
        </div>
        <div class="item-content">
          <p class="subtitle is-5">
            All data is encrypted using the Advanced Encryption Standard (AES)
            with a 256-bit key length. This encryption is done locally on your
            device before being sent to our servers.
          </p>
        </div>
      </div>
      <div class="item">
        <div class="item-title">
          <h3 class="title is-3">Key Derivation</h3>
        </div>
        <div class="item-content">
          <p class="subtitle is-5">
            Passwords are hashed using the Password-Based Key Derivation
            Function 2 (PBKDF2) with 600,000 iterations. This ensures that your
            data is secure and resistant to brute force attacks.
          </p>
        </div>
      </div>
      <div class="item">
        <div class="item-title">
          <h3 class="title is-3">Secure Storage</h3>
        </div>
        <div class="item-content">
          <p class="subtitle is-5">
            Your encrypted data is stored on our servers. However, it can only
            be decrypted with the proper key, which is derived from your account
            locally when you login.
          </p>
        </div>
      </div>
      <div class="item">
        <div class="item-title">
          <h3 class="title is-3">Two-Factor Authentication</h3>
        </div>
        <div class="item-content">
          <p class="subtitle is-5">
            Two-factor authentication (2FA) is used to add an extra layer of
            security to your account. This ensures that even if your password is
            compromised, your account remains secure.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.how-it-works {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 15%;
  text-align: center;
  gap: 2rem;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

.item {
  display: flex;
  flex-direction: column;
  align-items: start;
  text-align: start;
  justify-content: center;
}

.item-title .title {
  color: var(--bulma-text);
  padding: 0.5rem;
  border-image: linear-gradient(
      to right,
      var(--bulma-primary) 0%,
      var(--bulma-info) 100%
    )
    1;
  border-width: 0 0 4px 0;
  border-style: solid;
  padding: 5px;
}

.bold {
  font-weight: bold;
}

a:hover {
  border-bottom: 2px solid var(--bulma-primary);
}
</style>
