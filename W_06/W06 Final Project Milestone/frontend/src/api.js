/**
 * Cliente API para el backend FastAPI (Inventario + IA).
 * Configurado para producción en Render.
 */

import axios from 'axios'
import { getStoredToken, clearSession } from './lib/authStorage'

// URL DE PRODUCCIÓN (RENDER)
const API_URL = 'https://fons-inventory-backend.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  timeout: 20000, // 20 segundos de espera (la IA puede tardar un poco)
  headers: { 'Content-Type': 'application/json' },
})

// Interceptor: Inyectar Token de Supabase si existe
api.interceptors.request.use((config) => {
  const token = getStoredToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Interceptor: Manejar errores de sesión (401)
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      console.warn("Sesión caducada o inválida.")
      clearSession()
      // Opcional: Redirigir a login si usas react-router
      // window.location.href = '/login';
    }
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
    // Normalizamos: backend espera 'nombre' y 'cantidad'
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

export async function actualizarProducto(id, data) {
  try {
    const payload = {};
    
    // Validar cantidad
    let cantidadFinal = undefined;
    if (data.cantidad !== undefined) cantidadFinal = Number(data.cantidad);
    else if (data.quantity !== undefined) cantidadFinal = Number(data.quantity);
    
    if (cantidadFinal !== undefined) {
        payload.cantidad = cantidadFinal;
    }
    
    // Validar nombre
    if (data.nombre || data.name) {
        payload.nombre = data.nombre || data.name;
    }

    console.log(`[API] Actualizando ID Numérico: ${id} con payload:`, payload);

    // NOTA: 'id' aquí debe ser el número entero (ID de base de datos)
    const { data: res } = await api.put(`/productos/${id}`, payload)
    return res
  } catch (err) {
    console.error('[actualizarProducto]', err?.response?.data ?? err.message)
    throw err
  }
}

export async function eliminarProducto(id) {
  try {
    console.log(`[API] Eliminando ID Numérico: ${id}`);
    await api.delete(`/productos/${id}`)
  } catch (err) {
    console.error('[eliminarProducto]', err?.response?.data ?? err.message)
    throw err
  }
}

export default api