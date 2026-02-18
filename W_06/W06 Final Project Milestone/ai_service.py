"""
Servicio de IA para análisis de inventario usando Google Gemini.
Lee el inventario desde la base de datos (Supabase).
Si la API falla, devuelve un consejo por defecto basado en reglas simples.
"""

import os
from typing import TypedDict, List
from dotenv import load_dotenv
from pathlib import Path

# --- CORRECCIÓN CLAVE: Usamos la librería estándar instalada ---
import google.generativeai as genai

from database import get_session
from models import Product

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Modelos soportados por la librería estable
# Usamos gemini-pro como principal por estabilidad, y flash como backup
MODELOS_GEMINI = [
    "gemini-pro",
    "gemini-1.5-flash"
]

# Umbral bajo para considerar "poco stock"
UMBRAL_STOCK_BAJO = 10

class ProductoDict(TypedDict):
    """Representa un producto del inventario como diccionario."""
    product_id: str
    product_name: str
    quantity: int

def _obtener_productos_desde_db() -> List[ProductoDict]:
    """
    Abre una sesión nueva, consulta la tabla products y devuelve los datos actuales.
    """
    session = get_session()
    try:
        rows = session.query(Product).order_by(Product.product_id).all()
        productos = [
            {
                "product_id": p.product_id,
                "product_name": p.name,
                "quantity": p.quantity,
            }
            for p in rows
        ]
        return productos
    except Exception as e:
        print(f"[DB Error] Al leer productos: {e}")
        return []
    finally:
        session.close()

def _consejo_por_defecto(productos: List[ProductoDict]) -> str:
    """
    Genera un consejo simple basado en reglas (sin IA) para no romper la app.
    """
    if not productos:
        return "No hay productos registrados en la base de datos para analizar."

    en_cero = [p for p in productos if p["quantity"] == 0]
    bajos = [p for p in productos if 0 < p["quantity"] <= UMBRAL_STOCK_BAJO]

    partes: List[str] = []
    if en_cero:
        nombres = ", ".join(p["product_name"] for p in en_cero[:3])
        if len(en_cero) > 3: nombres += "..."
        partes.append(f"URGENTE: {nombres} están en cero.")
    
    if bajos:
        nombres = ", ".join(p["product_name"] for p in bajos[:3])
        partes.append(f"Poco stock: {nombres}.")
        
    if not partes:
        return "El inventario se ve saludable. ¡Buen trabajo manteniendo el stock!"

    return " ".join(partes) + " Revisa tu inventario completo."

def _formatear_inventario(productos: List[ProductoDict]) -> str:
    """Formatea la lista de productos para el prompt de Gemini."""
    return "\n".join(
        f"- {p['product_name']} (ID: {p['product_id']}): {p['quantity']} unid."
        for p in productos
    )

def generar_consejo_inventario() -> str:
    """
    Analiza el inventario con Gemini.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Error] Falta GEMINI_API_KEY")
        # Devolvemos fallback, pero necesitamos leer la DB primero para que tenga sentido
        productos = _obtener_productos_desde_db()
        return _consejo_por_defecto(productos)

    # 1. Obtener datos frescos
    productos = _obtener_productos_desde_db()
    if not productos:
        return "El inventario está vacío, agrega productos primero."

    # 2. Preparar Prompt
    texto_inventario = _formatear_inventario(productos)
    prompt = f"""
    Actúa como un experto en logística de tiendas minoristas.
    Analiza el siguiente inventario y dame UN SOLO consejo breve, práctico y directo para el dueño.
    Usa un tono amable pero profesional. No uses listas, solo un párrafo corto (máximo 2 oraciones).
    Si ves productos en 0, priorízalos.
    
    INVENTARIO:
    {texto_inventario}
    """

    # 3. Configurar IA (Sintaxis de librería Estable)
    genai.configure(api_key=api_key)

    # 4. Intentar generar respuesta
    for modelo in MODELOS_GEMINI:
        try:
            print(f"[IA] Intentando con modelo: {modelo}")
            model_instance = genai.GenerativeModel(modelo)
            response = model_instance.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
                
        except Exception as e:
            print(f"[IA Error] Falló {modelo}: {e}")
            continue # Intenta el siguiente modelo

    # 5. Si todo falla, usar fallback
    print("[IA] Todos los modelos fallaron, usando reglas manuales.")
    return _consejo_por_defecto(productos)