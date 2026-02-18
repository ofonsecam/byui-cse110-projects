"""
Configuración de conexión a la base de datos (Supabase/PostgreSQL) con SQLAlchemy.
Requiere DATABASE_URL en el entorno (cargar .env antes de importar).
Incluye validación de JWT de Supabase Auth para proteger endpoints.
"""
import os
import jwt
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Configuración de la Base de Datos
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL no está configurada en el archivo .env")

# Corrección para Render (Postgres requiere postgresql://)
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO DE PRODUCTO ---
class Product(Base):
    __tablename__ = "products"
    
    # id es la llave primaria NUMÉRICA (1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True)
    # product_id es el código de texto (P001, P002...)
    product_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# --- FUNCIONES DE BASE DE DATOS ---

def get_session():
    """Devuelve una nueva sesión de base de datos."""
    return SessionLocal()

def validate_jwt(token: str):
    """
    Decodifica el JWT de Supabase para obtener el usuario.
    Retorna el payload (dict) o None si es inválido.
    """
    try:
        secret = os.getenv("JWT_SECRET")
        if not secret:
            # Si no hay secreto configurado, asumimos modo desarrollo inseguro o fallamos
            print("[AUTH] Advertencia: JWT_SECRET no configurado.")
            return None
            
        # Supabase usa HS256 por defecto
        payload = jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
        return payload
    except Exception as e:
        print(f"[AUTH ERROR] {e}")
        return None

def create_product(session, name: str, quantity: int):
    """
    Crea un producto nuevo. Genera automáticamente el código P00X.
    """
    # 1. Buscar el último ID para generar el siguiente código
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
    """
    Actualiza un producto buscando por su ID NUMÉRICO (Primary Key).
    """
    # AQUI ESTABA EL ERROR: Buscamos por Product.id (número), NO por Product.product_id
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
    """
    Elimina un producto buscando por su ID NUMÉRICO.
    """
    product = session.query(Product).filter(Product.id == id_interno).first()
    
    if not product:
        return False
        
    session.delete(product)
    session.commit()
    return True