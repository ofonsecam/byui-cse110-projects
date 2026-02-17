/** Clave de localStorage para el token. Módulo separado para que api.js no importe React/Context. */
export const AUTH_TOKEN_KEY = 'inventory_auth_token'

export function getStoredToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY)
}

/** Limpia token y dispara evento para que AuthContext cierre sesión (p. ej. en 401). */
export function clearSession() {
  localStorage.removeItem(AUTH_TOKEN_KEY)
  window.dispatchEvent(new CustomEvent('auth:logout'))
}
