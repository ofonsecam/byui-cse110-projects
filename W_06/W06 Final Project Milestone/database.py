"""
Configuración de conexión a la base de datos (Supabase/PostgreSQL) con SQLAlchemy.
Requiere DATABASE_URL en el entorno (cargar .env antes de importar).
Incluye validación de JWT de Supabase Auth para proteger endpoints.
"""
import os
import jwt
from jwt import PyJWKClient # Cliente para bajar llaves de internet
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

# --- VALIDACIÓN DE TOKENS HÍBRIDA (HS256 + ES256) ---

def get_session():
    return SessionLocal()

def validate_jwt(token: str):
    """
    Valida el token intentando primero la llave pública (ES256/RS256) 
    y luego el secreto (HS256) como respaldo.
    """
    try:
        # 1. Intentar método moderno (ES256/RS256) usando JWKS de Supabase
        supabase_url = os.getenv("SUPABASE_URL") # Asegúrate que esta variable esté en Render
        if supabase_url:
            try:
                # Construimos la URL donde Supabase publica sus llaves
                jwks_url = f"{supabase_url}/.well-known/jwks.json"
                jwks_client = PyJWKClient(jwks_url)
                signing_key = jwks_client.get_signing_key_from_jwt(token)
                
                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["ES256", "RS256"],
                    audience="authenticated",
                    options={"verify_aud": False}
                )
                print("[AUTH SUCCESS] Token validado con JWKS (ES256/RS256)")
                return payload
            except Exception as e_jwks:
                # Si falla JWKS, no nos rendimos, probamos el método antiguo abajo
                print(f"[AUTH INFO] Falló validación JWKS: {e_jwks}. Intentando HS256...")

        # 2. Intentar método clásico (HS256) con JWT_SECRET
        secret = os.getenv("JWT_SECRET")
        if secret:
            payload = jwt.decode(
                token, 
                secret, 
                algorithms=["HS256"], 
                audience="authenticated",
                options={"verify_aud": False} 
            )
            print("[AUTH SUCCESS] Token validado con Secreto (HS256)")
            return payload
            
        print("[AUTH ERROR] No se pudo validar el token con ningún método.")
        return None

    except jwt.ExpiredSignatureError:
        print("[AUTH ERROR] El token ha expirado.")
        return None
    except jwt.InvalidSignatureError:
        print("[AUTH ERROR] La firma no es válida.")
        return None
    except Exception as e:
        print(f"[AUTH CRITICAL] Error inesperado validando token: {e}")
        return None

# --- FUNCIONES CRUD (Sin cambios) ---
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