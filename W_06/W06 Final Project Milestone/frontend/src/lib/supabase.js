/**
 * Cliente Supabase para autenticación.
 * Requiere VITE_SUPABASE_URL y VITE_SUPABASE_ANON_KEY en .env del frontend.
 */
import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!url || !anonKey) {
  console.warn('[supabase] Faltan VITE_SUPABASE_URL o VITE_SUPABASE_ANON_KEY en .env')
}

export const supabase = createClient(url || '', anonKey || '')
