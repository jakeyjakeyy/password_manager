import { useCookies } from "vue3-cookies";
import {
  deriveKey,
  encryptPassword,
  storeKey,
  deleteKey,
} from "@/utils/Cryptography";
const { cookies } = useCookies();

const accessToken = cookies.get("access_token");
const refreshToken = cookies.get("refresh_token");
const serverURL = import.meta.env.VITE_BACKEND_URL;

async function getSalt() {
  if (!accessToken) {
    return null;
  }
  const saltResponse = await fetch(`${serverURL}/api/salt`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const saltData = await saltResponse.json();
  return saltData.salt;
}

async function confirmRecovery(
  recovery: string,
  password: string,
  salt: string
) {
  // function to call the recovery API
  async function recoveryAPI(
    secret: string,
    verify: boolean,
    password?: Uint8Array,
    iv?: Uint8Array,
    username?: string | null
  ) {
    return fetch(`${serverURL}/api/recovery`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        iv: iv,
        password: password,
        secret: secret,
        username: username,
        verify: verify,
      }),
    });
  }
  // Derive the key from recovery secret
  const key = await deriveKey(recovery, salt);
  await storeKey(key);
  // Encrypt the password with our backup key
  const encrypted = await encryptPassword(password);
  const res = await recoveryAPI(
    recovery,
    false,
    encrypted.encryptedPassword,
    encrypted.iv,
    localStorage.getItem("username")
  );
  return res;
}

async function handleLogout() {
  await deleteKey();
  cookies.remove("access_token");
  cookies.remove("refresh_token");
  cookies.remove("salt");
  localStorage.removeItem("username");
  return 0;
}

export { confirmRecovery, getSalt, handleLogout };
