"""
Configuración de conexión a la base de datos (Supabase/PostgreSQL) con SQLAlchemy.
Requiere DATABASE_URL en el entorno (cargar .env antes de importar).
Incluye validación de JWT de Supabase Auth para proteger endpoints.
"""
import os
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# --- CONFIGURACIÓN DB ---
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    print("ADVERTENCIA: DB_URL no encontrada, usando sqlite local")
    DB_URL = "sqlite:///./inventory.db"

if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# --- VALIDACIÓN DE TOKENS ---

def get_session():
    return SessionLocal()

def validate_jwt(token: str):
    """
    Valida el token usando JWKS (llaves públicas de Supabase).
    Soporta ES256 (Nuevos proyectos) y RS256.
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        if not supabase_url:
            print("[AUTH ERROR] SUPABASE_URL no configurada en Render.")
            return None

        # --- CORRECCIÓN CRÍTICA: La ruta correcta incluye /auth/v1 ---
        # Limpiamos la URL base por si tiene slash al final
        base_url = supabase_url.rstrip("/")
        jwks_url = f"{base_url}/auth/v1/.well-known/jwks.json"

        try:
            jwks_client = PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
                options={"verify_aud": False}
            )
            # print("[AUTH SUCCESS] Token validado correctamente via JWKS") # Comentado para limpiar logs
            return payload
            
        except Exception as e_jwks:
            print(f"[AUTH ERROR] Falló JWKS en {jwks_url}: {e_jwks}")
            # Si falla JWKS con ES256, el método HS256 no servirá de nada, 
            # así que retornamos None directamente para ver el error real.
            return None

    except jwt.ExpiredSignatureError:
        print("[AUTH ERROR] El token ha expirado.")
        return None
    except Exception as e:
        print(f"[AUTH CRITICAL] Error inesperado: {e}")
        return None

# --- FUNCIONES CRUD ---
def create_product(session, name: str, quantity: int):
    last_product = session.query(Product).order_by(Product.id.desc()).first()
    if last_product and last_product.product_id.startswith("P"):
        try:
            last_num = int(last_product.product_id[1:])
            new_id_str = f"P{last_num + 1:03d}"
        except ValueError:
            new_id_str = "P001"
    else:
        new_id_str = "P001"
    new_product = Product(product_id=new_id_str, name=name, quantity=quantity)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

def update_product(session, id_interno: int, name: str = None, quantity: int = None):
    product = session.query(Product).filter(Product.id == id_interno).first()
    if not product: return None
    if name is not None: product.name = name
    if quantity is not None: product.quantity = quantity
    session.commit()
    session.refresh(product)
    return product

def delete_product(session, id_interno: int):
    product = session.query(Product).filter(Product.id == id_interno).first()
    if not product: return False
    session.delete(product)
    session.commit()
    return True