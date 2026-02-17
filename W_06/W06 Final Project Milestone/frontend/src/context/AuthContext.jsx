/**
 * Contexto de autenticación. Token en localStorage para persistir sesión al refrescar.
 * Login vía Supabase Auth; el backend valida el JWT con SUPABASE_JWT_SECRET.
 */
import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { supabase } from '../lib/supabase'
import { AUTH_TOKEN_KEY, clearSession } from '../lib/authStorage'

const AuthContext = createContext(null)

function parseJwtPayload(token) {
  try {
    const base64 = token.split('.')[1]
    if (!base64) return null
    return JSON.parse(atob(base64))
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const restoreSession = useCallback(() => {
    const token = localStorage.getItem(AUTH_TOKEN_KEY)
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    const payload = parseJwtPayload(token)
    setUser(payload ? { email: payload.email ?? payload.sub } : { email: 'Usuario' })
    setLoading(false)
  }, [])

  useEffect(() => {
    restoreSession()
  }, [restoreSession])

  useEffect(() => {
    const onLogout = () => setUser(null)
    window.addEventListener('auth:logout', onLogout)
    return () => window.removeEventListener('auth:logout', onLogout)
  }, [])

  const login = useCallback(async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
    const token = data?.session?.access_token
    if (token) {
      localStorage.setItem(AUTH_TOKEN_KEY, token)
      setUser({ email: data.user?.email ?? parseJwtPayload(token)?.email })
    }
  }, [])

  const logout = useCallback(() => {
    clearSession()
    setUser(null)
    supabase.auth.signOut().catch(() => {})
  }, [])

  const value = { user, loading, login, logout, isAuthenticated: !!user }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}

