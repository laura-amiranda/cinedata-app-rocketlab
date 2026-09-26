import { useEffect, useState } from 'react';

const TOKEN_KEY = 'notaflix_token';
const AUTH_EVENT = 'notaflix-auth-changed';

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
  window.dispatchEvent(new Event(AUTH_EVENT));
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
  window.dispatchEvent(new Event(AUTH_EVENT));
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}

/** Hook reativo: reflete login/logout em qualquer componente sem precisar recarregar a página. */
export function useIsAuthenticated(): boolean {
  const [authenticated, setAuthenticated] = useState(isAuthenticated());

  useEffect(() => {
    function handleChange() {
      setAuthenticated(isAuthenticated());
    }

    window.addEventListener(AUTH_EVENT, handleChange);
    return () => window.removeEventListener(AUTH_EVENT, handleChange);
  }, []);

  return authenticated;
}