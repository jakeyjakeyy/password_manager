import { useCookies } from "vue3-cookies";
import { jwtDecode } from "jwt-decode";
const { cookies } = useCookies();

async function RefreshToken() {
  const serverURL = import.meta.env.VITE_BACKEND_URL;
  const refresh = cookies.get("refresh_token");
  try {
    const response = await fetch(`${serverURL}/api/token/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh }),
    });

    const data = await response.json();

    if (data.detail === "Token is invalid or expired") {
      cookies.remove("refresh_token");
      cookies.remove("access_token");
      return { message: "Expired token" };
    }

    if (data.access) {
      cookies.set("access_token", data.access);
      return { message: "Token refreshed" };
    } else {
      return { message: "Please log in again" };
    }
  } catch (err) {
    console.log(err);
  }
}

function checkToken() {
  const refresh = cookies.get("access_token");
  if (!refresh) return false;
  const refreshDecoded = jwtDecode(refresh);
  const currentTime = Date.now() / 1000;
  if (refreshDecoded.exp && refreshDecoded.exp < currentTime) {
    deleteTokens();
    return false;
  }
  return true;
}

function deleteTokens() {
  cookies.remove("refresh_token");
  cookies.remove("access_token");
  cookies.remove("salt");
}

export { RefreshToken, checkToken, deleteTokens };
