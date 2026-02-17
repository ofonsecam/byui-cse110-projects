/**
 * Cliente API para el backend FastAPI (Inventario + IA).
 * Base URL: http://127.0.0.1:8000
 */

import axios from 'axios'
import { getStoredToken, clearSession } from './lib/authStorage'

const api = axios.create({
  baseURL: 'https://fons-inventory-backend.onrender.com', 
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = getStoredToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) clearSession()
    return Promise.reject(err)
  }
)

export async function getAnalizarInventario() {
  const { data } = await api.get('/analizar_inventario')
  return data
}

export async function getProductos() {
  try {
    const { data } = await api.get('/productos')
    return data
  } catch (err) {
    console.error('[getProductos]', err?.response?.data ?? err.message)
    throw err
  }
}

export async function crearProducto(data) {
  try {
    // AUDITORÍA: Aseguramos compatibilidad nombre/cantidad
    const payload = {
        nombre: data.nombre || data.name,
        cantidad: Number(data.cantidad !== undefined ? data.cantidad : data.quantity)
    }
    const { data: res } = await api.post('/productos', payload)
    return res
  } catch (err) {
    console.error('[crearProducto]', err?.response?.data ?? err.message)
    throw err
  }
}

// --- AQUÍ ESTABA EL PROBLEMA ---
export async function actualizarProducto(id, data) {
  try {
    // 1. Detectamos si viene 'cantidad' o 'quantity' y forzamos a Número
    let cantidadFinal = undefined;
    if (data.cantidad !== undefined) cantidadFinal = Number(data.cantidad);
    else if (data.quantity !== undefined) cantidadFinal = Number(data.quantity);

    // 2. Construimos el payload exacto que pide Python (ProductoUpdate)
    const payload = {};
    if (cantidadFinal !== undefined) {
        payload.cantidad = cantidadFinal; // Clave exacta 'cantidad'
    }
    if (data.nombre || data.name) {
        payload.nombre = data.nombre || data.name;
    }

    console.log(`[API] Actualizando ID: ${id} con payload:`, payload); // Log para depurar

    const { data: res } = await api.put(`/productos/${id}`, payload)
    return res
  } catch (err) {
    console.error('[actualizarProducto]', err?.response?.data ?? err.message)
    throw err
  }
}

export async function eliminarProducto(id) {
  try {
    await api.delete(`/productos/${id}`)
  } catch (err) {
    console.error('[eliminarProducto]', err?.response?.data ?? err.message)
    throw err
  }
}

export default api