"""
API FastAPI para análisis de inventario con IA.
Endpoint principal: GET /analizar_inventario
La API key se lee del entorno (archivo .env en la raíz del proyecto).
"""

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

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


def get_current_user(
    cred: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """Dependencia: exige Authorization: Bearer <JWT> válido (Supabase Auth). 401 si no hay token o es inválido."""
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
    description="Análisis de inventario con Gemini para recomendaciones.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RespuestaAnalisis(BaseModel):
    """Respuesta JSON del endpoint de análisis."""

    consejo: str
    ok: bool = True


class ProductoOut(BaseModel):
    """Producto para respuesta API. 'id' es la PK para PUT/DELETE."""

    id: int
    product_id: str
    name: str
    quantity: int


class ProductoCreate(BaseModel):
    """Payload para crear producto. Cantidad no puede ser negativa."""

    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del producto")
    cantidad: int = Field(..., ge=0, description="Cantidad en inventario (>= 0)")


class ProductoUpdate(BaseModel):
    """Payload para actualizar producto. Campos opcionales; cantidad >= 0 si se envía."""

    nombre: str | None = Field(None, min_length=1, max_length=255)
    cantidad: int | None = Field(None, ge=0)


class MensajeOut(BaseModel):
    """Respuesta genérica para el frontend."""

    message: str
    ok: bool = True


@app.get("/analizar_inventario", response_model=RespuestaAnalisis)
def analizar_inventario() -> RespuestaAnalisis:
    """
    Lee el inventario desde la base de datos (Supabase), lo analiza con Gemini y devuelve un consejo.
    """
    try:
        consejo = generar_consejo_inventario()
        return RespuestaAnalisis(consejo=consejo)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar el inventario: {e!s}",
        )


@app.get("/productos", response_model=list[ProductoOut])
def listar_productos() -> list[ProductoOut]:
    """Lista todos los productos del inventario desde Supabase."""
    session = get_session()
    try:
        rows = session.query(Product).order_by(Product.product_id).all()
        return [ProductoOut(id=p.id, product_id=p.product_id, name=p.name, quantity=p.quantity) for p in rows]
    finally:
        session.close()


@app.post("/productos", response_model=ProductoOut, status_code=201)
def crear_producto(body: ProductoCreate, user: dict = Depends(get_current_user)) -> ProductoOut:
    """Crea un nuevo producto (nombre y cantidad). Cantidad >= 0."""
    session = get_session()
    try:
        product = create_product(session, body.nombre, body.cantidad)
        return ProductoOut(id=product.id, product_id=product.product_id, name=product.name, quantity=product.quantity)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": f"Datos inválidos: {e!s}", "ok": False})
    finally:
        session.close()


# Cambiamos {id} a {product_id} para ser más precisos, o simplemente cambiamos el tipo
@app.put("/productos/{id}", response_model=ProductoOut)
def actualizar_producto(
    id: str,  # <--- ¡AQUÍ ESTABA EL ERROR! Antes decía 'int', ahora debe ser 'str'
    body: ProductoUpdate, 
    user: dict = Depends(get_current_user)
) -> ProductoOut:
    """Actualiza nombre y/o cantidad de un producto existente. 404 si no existe."""
    
    if body.nombre is None and body.cantidad is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Debe enviar al menos 'nombre' o 'cantidad' para actualizar", "ok": False},
        )
    
    session = get_session()
    try:
        # Pasamos 'id' (que ahora es string "P001") a tu función de base de datos
        product = update_product(session, id, name=body.nombre, quantity=body.cantidad)
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail={"message": f"Producto con id {id} no encontrado", "ok": False},
            )
            
        return ProductoOut(
            id=product.id, 
            product_id=product.product_id, 
            name=product.name, 
            quantity=product.quantity
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": f"Datos inválidos: {e!s}", "ok": False})
    finally:
        session.close()


@app.delete("/productos/{id}", response_model=MensajeOut)
def eliminar_producto(id: int, user: dict = Depends(get_current_user)) -> MensajeOut:
    """Elimina un producto por id. 404 si no existe."""
    session = get_session()
    try:
        deleted = delete_product(session, id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail={"message": f"Producto con id {id} no encontrado", "ok": False},
            )
        return MensajeOut(message=f"Producto con id {id} eliminado correctamente")
    except HTTPException:
        raise
    finally:
        session.close()


@app.get("/health")
def health() -> dict[str, str]:
    """Health check para despliegue."""
    return {"status": "ok"}
