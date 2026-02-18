"""
Configuración de conexión a la base de datos (Supabase/PostgreSQL) con SQLAlchemy.
Requiere DATABASE_URL en el entorno (cargar .env antes de importar).
Incluye validación de JWT de Supabase Auth para proteger endpoints.
"""
import os
import jwt  # Esta es la librería PyJWT
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Configuración de la Base de Datos
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    # Fallback por si la variable no carga, evita crash inmediato
    print("ADVERTENCIA: DB_URL no encontrada, usando sqlite local por defecto")
    DB_URL = "sqlite:///./inventory.db"

# Corrección para Render (Postgres requiere postgresql://)
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO DE PRODUCTO ---
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)

# Crear tablas (Sin drop_all para seguridad en producción)
Base.metadata.create_all(bind=engine)

# --- FUNCIONES DE BASE DE DATOS ---

def get_session():
    """Devuelve una nueva sesión de base de datos."""
    return SessionLocal()

def validate_jwt(token: str):
    """
    Decodifica el JWT de Supabase con diagnóstico avanzado.
    """
    try:
        secret = os.getenv("JWT_SECRET")
        if not secret:
            print("[AUTH ERROR] JWT_SECRET no está configurado en Render.")
            return None
            
        # 1. DIAGNÓSTICO: Leer el encabezado del token sin verificar firma
        # Esto nos dirá qué algoritmo está usando Supabase realmente.
        try:
            header = jwt.get_unverified_header(token)
            algoritmo_recibido = header.get('alg')
            print(f"[AUTH DEBUG] Algoritmo del Token: {algoritmo_recibido}")
        except Exception as e:
            print(f"[AUTH ERROR] Token corrupto o ilegible: {e}")
            return None

        # 2. DECODIFICACIÓN TOLERANTE
        # Permitimos HS256 (Defecto) y RS256 (Configuraciones avanzadas)
        # Nota: options={"verify_aud": False} ayuda si la audiencia no coincide exactamente.
        payload = jwt.decode(
            token, 
            secret, 
            algorithms=["HS256", "RS256"], 
            audience="authenticated",
            options={"verify_aud": False} 
        )
        return payload

    except jwt.ExpiredSignatureError:
        print("[AUTH ERROR] El token ha expirado.")
        return None
    except jwt.InvalidSignatureError:
        print("[AUTH ERROR] La firma del token no coincide con el JWT_SECRET.")
        return None
    except Exception as e:
        print(f"[AUTH CRITICAL ERROR] {e}")
        return None

def create_product(session, name: str, quantity: int):
    # Generar ID P00X basado en el último registro
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
    # Buscar por ID numérico
    product = session.query(Product).filter(Product.id == id_interno).first()
    if not product:
        return None
    if name is not None:
        product.name = name
    if quantity is not None:
        product.quantity = quantity
    session.commit()
    session.refresh(product)
    return product

def delete_product(session, id_interno: int):
    # Borrar por ID numérico
    product = session.query(Product).filter(Product.id == id_interno).first()
    if not product:
        return False
    session.delete(product)
    session.commit()
    return True