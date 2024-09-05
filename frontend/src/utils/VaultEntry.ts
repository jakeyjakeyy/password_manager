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
    if (refresh.error) {
      return Add(password, username, name);
    } else {
      alert("Log in again");
    }
  }
  return response.json();
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
    if (refresh.error) {
      return AddBatch(entries);
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}

async function AddFile(
  encryptedFile: Uint8Array,
  iv: any,
  name: string,
  entry: number
) {
  const res = await fetch(`${serverURL}/api/vault/files/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({
      id: entry,
      file: encryptedFile,
      iv: iv,
      name: name,
    }),
  });
  if (res.status === 401) {
    const refresh = await RefreshToken();
    if (refresh.error) {
      return AddFile(encryptedFile, iv, name, entry);
    } else {
      alert("Log in again");
    }
  }
  return res.json();
}

async function DeleteFile(id: number) {
  const response: any = await fetch(`${serverURL}/api/vault/files/delete`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({ id: id }),
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh.error) {
      return DeleteFile(id);
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}

async function Delete(id: string) {
  const response: any = await fetch(`${serverURL}/api/vault/delete`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({ id: id }),
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh.error) {
      return Delete(id);
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}

async function Edit(
  id: string,
  password: string,
  username: string,
  name: string
) {
  const key = await Cryptography.retrieveKey();
  const encrypted = await Cryptography.encryptPassword(password);
  const encryptedPassword = encrypted.encryptedPassword;
  const iv = encrypted.iv;

  const response: any = await fetch(`${serverURL}/api/vault/edit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({
      id: id,
      password: encryptedPassword,
      iv: iv,
      username: username,
      name: name,
    }),
  });
  if (response.status === 401) {
    const refresh = await RefreshToken();
    if (refresh.error) {
      return Edit(id, password, username, name);
    } else {
      alert("Log in again");
    }
  }
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
    if (refresh.error) {
      return Retrieve();
    } else {
      alert("Log in again");
    }
  }
  return response.json();
}
export { Add, AddBatch, Edit, Delete, Retrieve, AddFile, DeleteFile };
