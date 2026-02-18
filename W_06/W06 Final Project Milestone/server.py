"""
API FastAPI para análisis de inventario con IA.
Configurada para despliegue en Render y conexión con Vercel.
"""

from dotenv import load_dotenv
from pathlib import Path
import os

# Carga variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Optional

# Importaciones locales (Asegúrate de que estos archivos existan)
from ai_service import generar_consejo_inventario
from database import (
    create_product,
    delete_product,
    get_session,
    update_product,
    validate_jwt,
)
from models import Product

security = HTTPBearer(auto_error=False)

def get_current_user(cred: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
    """Valida el token JWT de Supabase."""
    if cred is None or not cred.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Falta token de autorización", "ok": False},
        )
    user = validate_jwt(cred.credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token inválido o expirado", "ok": False},
        )
    return user

app = FastAPI(
    title="API Inventario + IA",
    description="Backend Fons Inventory - Render Deploy",
    version="1.1.0",
)

# --- CONFIGURACIÓN CORS ---
# Esto permite que Vercel hable con este servidor
origins = [
    "http://localhost:5173", # Desarrollo local Vite
    "http://localhost:3000", # Desarrollo local React
    "https://fons-inventory.vercel.app", # Producción (TU APP)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS PYDANTIC ---

class RespuestaAnalisis(BaseModel):
    consejo: str
    ok: bool = True

class ProductoOut(BaseModel):
    id: int
    product_id: str
    name: str
    quantity: int
    
    class Config:
        from_attributes = True

class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    cantidad: int = Field(..., ge=0)

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    cantidad: Optional[int] = Field(None, ge=0)

class MensajeOut(BaseModel):
    message: str
    ok: bool = True

# --- ENDPOINTS ---

@app.get("/health")
def health():
    return {"status": "ok", "service": "Fons Inventory Backend"}

@app.get("/analizar_inventario", response_model=RespuestaAnalisis)
def analizar_inventario():
    try:
        consejo = generar_consejo_inventario()
        return RespuestaAnalisis(consejo=consejo)
    except Exception as e:
        print(f"Error IA: {e}")
        raise HTTPException(status_code=500, detail=f"Error IA: {str(e)}")

@app.get("/productos", response_model=List[ProductoOut])
def listar_productos():
    session = get_session()
    try:
        rows = session.query(Product).order_by(Product.id).all()
        # Mapeamos la respuesta usando el modelo ProductoOut
        return [ProductoOut(id=p.id, product_id=p.product_id, name=p.name, quantity=p.quantity) for p in rows]
    except Exception as e:
        print(f"Error DB: {e}")
        raise HTTPException(status_code=500, detail="Error al leer base de datos")
    finally:
        session.close()

@app.post("/productos", response_model=ProductoOut, status_code=201)
def crear_producto(body: ProductoCreate, user: dict = Depends(get_current_user)):
    session = get_session()
    try:
        # create_product en database.py debe manejar la creación del código "P00X"
        product = create_product(session, body.nombre, body.cantidad)
        return product
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear: {str(e)}")
    finally:
        session.close()

@app.put("/productos/{id}", response_model=ProductoOut)
def actualizar_producto(id: int, body: ProductoUpdate, user: dict = Depends(get_current_user)):
    """
    Actualiza por ID numérico (Primary Key). 
    Es más seguro usar el ID entero que el string 'P001' para evitar errores de URL.
    """
    if body.nombre is None and body.cantidad is None:
        raise HTTPException(status_code=400, detail="Enviar nombre o cantidad")
    
    session = get_session()
    try:
        # Llama a la función de base de datos pasando el ID entero
        product = update_product(session, id, name=body.nombre, quantity=body.cantidad)
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
            
        return product
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar: {str(e)}")
    finally:
        session.close()

@app.delete("/productos/{id}", response_model=MensajeOut)
def eliminar_producto(id: int, user: dict = Depends(get_current_user)):
    session = get_session()
    try:
        deleted = delete_product(session, id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return MensajeOut(message=f"Producto {id} eliminado")
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()