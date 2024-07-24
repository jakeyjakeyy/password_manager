import * as Cryptography from "@/utils/Cryptography";
import { RefreshToken } from "./RefreshToken";
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
const serverURL = import.meta.env.VITE_BACKEND_URL;

async function Add(password: string, username: string, name: string) {
  const key = await Cryptography.retrieveKey();
  const encrypted = await Cryptography.encryptPassword(password);
  const encryptedPassword = encrypted.encryptedPassword;
  const iv = encrypted.iv;

  const response: any = await fetch(`${serverURL}/api/vault/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({
      password: encryptedPassword,
      iv: iv,
      username: username,
      name: name,
    }),
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh) {
      return Add(password, username, name);
    } else {
      alert("Log in again");
    }
  }
}

async function AddBatch(entries: any) {
  const response: any = await fetch(`${serverURL}/api/vault/add-batch`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({ entries: entries }),
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh) {
      return AddBatch(entries);
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}

async function Retrieve() {
  const response: any = await fetch(`${serverURL}/api/vault/retrieve`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh) {
      return Retrieve();
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}
export { Add, AddBatch, Retrieve };
