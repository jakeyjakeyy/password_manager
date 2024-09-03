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

async function deleteKey() {
  const db = await openDB("myDatabase", 1);
  await db.delete("keys", "encryptionKey");
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

async function encryptPassword(plainPassword: string) {
  const key = await retrieveKey();
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

async function decryptPassword(encryptedPassword: Uint8Array, iv: Uint8Array) {
  const key = await retrieveKey();
  const encryptedPasswordBuffer = objectToUint8Array(encryptedPassword);
  const ivBuffer = objectToUint8Array(iv);
  const decrypted = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: ivBuffer,
    },
    key,
    encryptedPasswordBuffer
  );
  const decoder = new TextDecoder();
  return decoder.decode(decrypted);
}

function objectToUint8Array(obj: any) {
  const arr = new Uint8Array(Object.keys(obj).length);
  for (let i = 0; i < arr.length; i++) {
    arr[i] = obj[i];
  }
  return arr;
}

async function encryptFile(file: File) {
  const key = await retrieveKey();
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await window.crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: iv,
    },
    key,
    await file.arrayBuffer()
  );
  const encryptedFile = new Uint8Array(encrypted);

  return {
    encryptedFile: encryptedFile,
    iv: iv,
  };
}

async function decryptFile(file: Uint8Array, iv: Uint8Array, name: string) {
  const key = await retrieveKey();
  const ivBuffer = objectToUint8Array(iv);
  const decrypted = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: ivBuffer,
    },
    key,
    file
  );

  const decryptedFile = new File([new Uint8Array(decrypted)], name);

  return decryptedFile;
}

export {
  deriveKey,
  storeKey,
  deleteKey,
  retrieveKey,
  encryptPassword,
  decryptPassword,
  encryptFile,
  decryptFile,
};
