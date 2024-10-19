import { openDB, deleteDB } from "idb";

async function deriveKey(
  masterPassword: string,
  salt: string,
  iterations = 600000,
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
  await deleteDB("vault");
  const db = await openDB("vault", 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains("keys")) {
        db.createObjectStore("keys", { keyPath: "id" });
      }
    },
  });

  await db.add("keys", {
    id: "encryptionKey",
    key: await window.crypto.subtle.exportKey("jwk", key),
  });
}

async function deleteKey() {
  deleteDB("vault");
}

async function retrieveKey() {
  const db = await openDB("vault");
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
  try {
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
  } catch (e) {
    console.log(e);
  }
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
  const fileBuffer = objectToUint8Array(file);
  const key = await retrieveKey();
  const ivBuffer = objectToUint8Array(iv);
  const decrypted = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: ivBuffer,
    },
    key,
    fileBuffer
  );

  const decryptedFile = new File([new Uint8Array(decrypted)], name);

  // // trigger file download
  // const url = URL.createObjectURL(decryptedFile);
  // const a = document.createElement("a");
  // a.href = url;
  // a.download = name;
  // a.click();

  return decryptedFile;
}

function generateRecoverySecret() {
  const array = new Uint8Array(32);
  window.crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array));
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
  generateRecoverySecret,
  objectToUint8Array,
};
