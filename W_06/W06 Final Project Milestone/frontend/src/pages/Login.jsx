/**
 * Página de Login. Formulario email/contraseña con Supabase Auth.
 * Tailwind CSS. Mensaje de error y estado de carga.
 */
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { LogIn } from 'lucide-react'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email.trim(), password)
    } catch (err) {
      setError(err?.message ?? 'Error al iniciar sesión. Revisa email y contraseña.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-sm rounded-2xl bg-white shadow-xl border border-slate-200 p-8">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-slate-800">
            Fons Inventory
          </h1>
          <p className="text-slate-500 text-sm mt-1">Inicia sesión para continuar</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="login-email" className="block text-sm font-medium text-slate-700 mb-1">
              Correo electrónico
            </label>
            <input
              id="login-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              autoComplete="email"
              required
              disabled={loading}
              className="w-full min-h-[48px] rounded-xl border-2 border-slate-200 px-4 text-slate-800 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 outline-none transition disabled:opacity-50"
            />
          </div>
          <div>
            <label htmlFor="login-password" className="block text-sm font-medium text-slate-700 mb-1">
              Contraseña
            </label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="current-password"
              required
              disabled={loading}
              className="w-full min-h-[48px] rounded-xl border-2 border-slate-200 px-4 text-slate-800 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 outline-none transition disabled:opacity-50"
            />
          </div>
          {error && (
            <p className="text-red-600 text-sm font-medium" role="alert">
              {error}
            </p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full min-h-[52px] flex items-center justify-center gap-2 rounded-xl font-semibold text-white bg-amber-500 hover:bg-amber-600 active:bg-amber-700 shadow-md disabled:opacity-50 transition"
          >
            <LogIn className="w-5 h-5" aria-hidden />
            {loading ? 'Entrando…' : 'Iniciar sesión'}
          </button>
        </form>
      </div>
    </div>
  )
}
