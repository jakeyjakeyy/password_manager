import { openDB } from "idb";

function deriveKey(
  masterPassword: string,
  salt: string,
  iterations = 100000,
  keyLength = 256
) {
  const encoder = new TextEncoder();
  return window.crypto.subtle
    .importKey(
      "raw",
      encoder.encode(masterPassword),
      { name: "PBKDF2" },
      false,
      ["deriveKey"]
    )
    .then((baseKey) => {
      return window.crypto.subtle.deriveKey(
        {
          name: "PBKDF2",
          salt: encoder.encode(salt),
          iterations: iterations,
          hash: "SHA-256",
        },
        baseKey,
        { name: "AES-GCM", length: keyLength },
        true,
        ["encrypt", "decrypt"]
      );
    });
}

async function storeKey(key: CryptoKey) {
  const db = await openDB("myDatabase", 1, {
    upgrade(db) {
      db.createObjectStore("keys", { keyPath: "id" });
    },
  });

  // Delete the old key if it exists
  await db.delete("keys", "encryptionKey");

  await db.add("keys", {
    id: "encryptionKey",
    key: await window.crypto.subtle.exportKey("jwk", key),
  });
}

async function retrieveKey() {
  const db = await openDB("myDatabase", 1);
  const keyData = await db.get("keys", "encryptionKey");
  return window.crypto.subtle.importKey(
    "jwk",
    keyData.key,
    { name: "AES-GCM" },
    true,
    ["encrypt", "decrypt"]
  );
}

async function encryptPassword(plainPassword: string, key: CryptoKey) {
  const encoder = new TextEncoder();
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await window.crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: iv,
    },
    key,
    encoder.encode(plainPassword)
  );
  return {
    iv: iv,
    encryptedPassword: new Uint8Array(encrypted),
  };
}

async function decryptPassword(
  encryptedPassword: Uint8Array,
  iv: Uint8Array,
  key: CryptoKey
) {
  const decrypted = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: iv,
    },
    key,
    encryptedPassword
  );
  const decoder = new TextDecoder();
  return decoder.decode(decrypted);
}

export { deriveKey, storeKey, retrieveKey, encryptPassword, decryptPassword };
