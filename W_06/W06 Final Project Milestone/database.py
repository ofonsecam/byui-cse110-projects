"""
Configuración de conexión a la base de datos (Supabase/PostgreSQL) con SQLAlchemy.
Requiere DATABASE_URL en el entorno (cargar .env antes de importar).
Incluye validación de JWT de Supabase Auth para proteger endpoints.
"""

import os
from pathlib import Path

import jwt
import requests
from jwt import PyJWKClient
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or not DATABASE_URL.strip():
    raise ValueError("DATABASE_URL no está definida en el entorno (.env)")

# Supabase puede devolver postgres://; psycopg2 requiere postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SUPABASE_URL = "https://prtxahssrpalfhnhuxkj.supabase.co"


def get_db() -> Session:
    """Generador de sesión para uso en endpoints o scripts. Cerrar con session.close()."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """Devuelve una sesión activa. El llamador debe hacer session.close() al terminar."""
    return SessionLocal()


def get_product_by_id(session: Session, id: int):
    """Devuelve el producto por PK id o None si no existe."""
    from models import Product
    return session.get(Product, id)


def create_product(session: Session, name: str, quantity: int):
    """
    Crea un producto en public.products. Genera product_id único.
    Hace commit. Devuelve el Product creado.
    """
    import uuid
    from models import Product
    product_id = "P" + uuid.uuid4().hex[:10].upper()
    product = Product(product_id=product_id, name=name.strip(), quantity=quantity)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(session, product_id_str, name=None, quantity=None):
    # AUDITORÍA: Importamos el modelo aquí dentro para evitar el error "Product is not defined"
    from models import Product 
    
    # Buscamos explícitamente en la columna 'product_id' (el código de texto "P001")
    # en lugar de la llave primaria numérica (id)
    product = session.query(Product).filter(Product.product_id == product_id_str).first()
    
    if not product:
        return None
        
    # Actualizamos solo los campos que no sean None
    if name is not None:
        product.name = name
    if quantity is not None:
        product.quantity = quantity
        
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: Session, id: int) -> bool:
    """Elimina el producto con PK id. Devuelve True si existía y se eliminó."""
    from models import Product
    product = session.get(Product, id)
    if not product:
        return False
    session.delete(product)
    session.commit()
    return True


def validate_jwt(access_token: str) -> dict | None:
    """
    Valida el JWT emitido por Supabase Auth usando JWKS del proyecto (llave pública desde la URL).
    Returns:
        Payload del token con sub, email, etc. si es válido; None si falla.
    """
    try:
        jwks_url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)

        payload = jwt.decode(
            access_token.strip(),
            signing_key.key,
            algorithms=["HS256", "ES256"],
            audience="authenticated"
        )
        return payload
    except Exception as e:
        print(f"ERROR DE SEGURIDAD: {str(e)}")
        return None
        
