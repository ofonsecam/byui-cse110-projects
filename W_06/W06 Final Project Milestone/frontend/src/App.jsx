import { useState, useEffect } from 'react'
import { Trash2, Plus, LogOut, Sparkles } from 'lucide-react'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import {
  getAnalizarInventario,
  getProductos,
  actualizarProducto,
  eliminarProducto,
  crearProducto,
} from './api'
import './App.css'

function App() {
  const { isAuthenticated, loading, user, logout } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <p className="text-slate-600">Cargando…</p>
      </div>
    )
  }
  if (!isAuthenticated) {
    return <Login />
  }

  return <InventoryApp user={user} onLogout={logout} />
}

function InventoryApp({ user, onLogout }) {
  const [consejo, setConsejo] = useState('Presiona el botón para recibir un análisis de tu inventario.')
  const [consejoLoading, setConsejoLoading] = useState(false)
  const [consejoError, setConsejoError] = useState(null)
  const [productos, setProductos] = useState([])
  const [productosLoading, setProductosLoading] = useState(true)
  const [productosError, setProductosError] = useState(null)
  const [editingQuantity, setEditingQuantity] = useState({})
  const [confirmingDeleteId, setConfirmingDeleteId] = useState(null)
  const [updateError, setUpdateError] = useState(null)
  const [modalAgregarOpen, setModalAgregarOpen] = useState(false)
  const [formNombre, setFormNombre] = useState('')
  const [formCantidad, setFormCantidad] = useState('')
  const [addError, setAddError] = useState(null)
  const [addLoading, setAddLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState(null)

  // FUNCIÓN NUEVA: Controla manualmente la petición a Gemini para ahorrar cuota
  const solicitarAnalisisIA = () => {
    setConsejoLoading(true)
    setConsejoError(null)
    getAnalizarInventario()
      .then((res) => {
        setConsejo(res.consejo ?? 'No hay consejos disponibles en este momento.')
      })
      .catch((err) => {
        setConsejoError(err.response?.status === 429 
          ? 'Cuota de IA agotada. Por favor, intenta de nuevo en un minuto.' 
          : 'Error al conectar con la IA.')
      })
      .finally(() => setConsejoLoading(false))
  }

  useEffect(() => {
    getProductos()
      .then((res) => setProductos(Array.isArray(res) ? res : []))
      .catch((err) => {
        setProductosError(err.message || 'Error al cargar productos')
        setProductos([])
      })
      .finally(() => setProductosLoading(false))
  }, [])

  const handleQuantityBlur = (productId, inputValue) => {
    const n = parseInt(String(inputValue).trim(), 10)
    if (isNaN(n) || n < 0) return
    
    setEditingQuantity((prev) => {
      const next = { ...prev }
      delete next[productId]
      return next
    })
    
    setUpdateError(null)
    actualizarProducto(productId, { cantidad: n })
      .then(() => {
        setProductos((prev) =>
          prev.map((p) =>
            p.product_id === productId ? { ...p, quantity: n } : p
          )
        )
      })
      .catch((err) => {
        setUpdateError(err.message || 'Error al actualizar')
      })
  }

  const handleDeleteConfirm = (productId) => {
    setUpdateError(null)
    eliminarProducto(productId)
      .then(() => {
        setProductos((prev) => prev.filter((p) => p.product_id !== productId))
        setConfirmingDeleteId(null)
      })
      .catch((err) => {
        setUpdateError(err.message || 'Error al eliminar')
      })
  }

  const openModalAgregar = () => {
    setFormNombre('')
    setFormCantidad('')
    setAddError(null)
    setModalAgregarOpen(true)
  }

  const closeModalAgregar = () => {
    if (!addLoading) {
      setModalAgregarOpen(false)
      setAddError(null)
    }
  }

  const handleAgregarSubmit = (e) => {
    e.preventDefault()
    const nombre = formNombre.trim()
    const cantidadRaw = formCantidad === '' ? NaN : Number(formCantidad)
    if (!nombre) {
      setAddError('El nombre del producto no puede estar vacío.')
      return
    }
    if (Number.isNaN(cantidadRaw) || cantidadRaw < 0) {
      setAddError('La cantidad debe ser un número mayor o igual a 0.')
      return
    }
    setAddError(null)
    setAddLoading(true)
    
    crearProducto({ nombre, cantidad: Math.floor(cantidadRaw) })
      .then(() => {
        setModalAgregarOpen(false)
        setFormNombre('')
        setFormCantidad('')
        setSuccessMessage('Producto agregado con éxito.')
        setTimeout(() => setSuccessMessage(null), 4000)
        return getProductos() // AUDITORÍA: Ya NO llamamos a getAnalizarInventario aquí automáticamente
      })
      .then((list) => {
        setProductos(Array.isArray(list) ? list : [])
      })
      .catch((err) => {
        setAddError(err.response?.data?.detail || 'Error al agregar producto.')
      })
      .finally(() => setAddLoading(false))
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 pb-8">
      <header className="bg-slate-800 text-white py-4 px-4 shadow-md flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-bold">Fons Inventory</h1>
        <div className="flex items-center gap-3">
          <span className="text-slate-300 text-sm hidden sm:inline">{user?.email}</span>
          <button onClick={onLogout} className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-600 text-sm font-medium">
            <LogOut className="w-4 h-4" /> Salir
          </button>
        </div>
      </header>

      {successMessage && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-3 rounded-lg shadow-lg bg-emerald-600 text-white text-sm font-medium">
          {successMessage}
        </div>
      )}

      <main className="max-w-4xl mx-auto px-4 pt-6 space-y-6">
        {/* SECCIÓN IA OPTIMIZADA */}
        <section className="rounded-xl p-5 shadow-lg border-2 border-amber-400 bg-white text-slate-900">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
            <h2 className="text-base font-bold flex items-center gap-2 text-amber-600">
              <Sparkles className="w-5 h-5" /> Análisis del Inventario
            </h2>
            <button 
              onClick={solicitarAnalisisIA}
              disabled={consejoLoading}
              className="px-4 py-2 bg-amber-500 text-white rounded-lg text-sm font-bold shadow hover:bg-amber-600 disabled:opacity-50 flex items-center gap-2"
            >
              {consejoLoading ? 'Analizando...' : 'Actualizar Consejo IA'}
            </button>
          </div>
          
          <div className="p-4 rounded-lg bg-amber-50 border border-amber-200">
            {consejoError && (
              <p className="text-red-600 text-sm font-medium">{consejoError}</p>
            )}
            {!consejoError && (
              <p className="text-sm sm:text-base leading-relaxed text-slate-700 italic">
                "{consejo}"
              </p>
            )}
          </div>
        </section>

        <div className="flex items-center justify-between gap-3 px-1">
          <h2 className="text-lg font-semibold text-slate-700">Productos</h2>
          <button onClick={openModalAgregar} className="flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md">
            <Plus className="w-5 h-5" /> Agregar
          </button>
        </div>

        {updateError && <p className="text-red-600 text-sm font-medium px-1">{updateError}</p>}

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {productos.map((p) => {
            const isConfirming = confirmingDeleteId === p.product_id
            const displayQty = editingQuantity[p.product_id] !== undefined ? editingQuantity[p.product_id] : p.quantity
            const isZero = parseInt(String(displayQty), 10) === 0

            return (
              <article key={p.product_id} className={`rounded-xl p-5 shadow-md bg-white border-2 flex flex-col ${isZero ? 'border-red-500' : 'border-slate-200'}`}>
                <h3 className="font-semibold text-slate-800 text-base mb-1">{p.name}</h3>
                <p className="text-slate-500 text-xs mb-2">ID: {p.product_id}</p>

                {!isConfirming ? (
                  <>
                    <div className="mt-auto space-y-2">
                      <label className="block text-sm font-medium text-slate-600">Cantidad</label>
                      <input
                        type="number"
                        min={0}
                        value={displayQty}
                        onChange={(e) => setEditingQuantity((prev) => ({ ...prev, [p.product_id]: e.target.value }))}
                        onBlur={(e) => handleQuantityBlur(p.product_id, e.target.value)}
                        className={`w-full min-h-[48px] text-lg font-bold rounded-lg border-2 px-3 ${isZero ? 'border-red-400 text-red-600 bg-red-50' : 'border-slate-300 text-slate-700'}`}
                      />
                    </div>
                    <button onClick={() => setConfirmingDeleteId(p.product_id)} className="mt-3 w-full py-2 flex items-center justify-center gap-2 rounded-lg border-2 border-red-200 bg-red-50 text-red-700 font-medium">
                      <Trash2 className="w-4 h-4" /> Eliminar
                    </button>
                  </>
                ) : (
                  <div className="mt-auto space-y-3">
                    <p className="text-slate-700 font-medium text-sm text-center">¿Eliminar producto?</p>
                    <div className="flex gap-2">
                      <button onClick={() => setConfirmingDeleteId(null)} className="flex-1 py-2 rounded-lg border-2 border-slate-300 bg-slate-100 text-sm">No</button>
                      <button onClick={() => handleDeleteConfirm(p.product_id)} className="flex-1 py-2 rounded-lg bg-red-500 text-white text-sm font-bold">Sí</button>
                    </div>
                  </div>
                )}
              </article>
            )
          })}
        </div>
      </main>

      {modalAgregarOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center p-4 bg-slate-900/60" onClick={closeModalAgregar}>
          <div className="w-full max-w-sm rounded-xl bg-white shadow-xl border-2 border-slate-200 p-5" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Agregar producto</h3>
            <form onSubmit={handleAgregarSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre</label>
                <input type="text" value={formNombre} onChange={(e) => setFormNombre(e.target.value)} className="w-full h-12 rounded-lg border-2 border-slate-300 px-3" disabled={addLoading} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Cantidad Inicial</label>
                <input type="number" min={0} value={formCantidad} onChange={(e) => setFormCantidad(e.target.value)} className="w-full h-12 rounded-lg border-2 border-slate-300 px-3" disabled={addLoading} />
              </div>
              {addError && <p className="text-red-600 text-sm font-medium">{addError}</p>}
              <div className="flex gap-2">
                <button type="button" onClick={closeModalAgregar} disabled={addLoading} className="flex-1 h-12 rounded-lg border-2 border-slate-300 bg-slate-50">Cancelar</button>
                <button type="submit" disabled={addLoading} className="flex-1 h-12 rounded-lg bg-emerald-600 text-white font-bold">{addLoading ? '...' : 'Guardar'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App