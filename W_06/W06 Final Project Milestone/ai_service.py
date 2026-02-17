"""
Servicio de IA para análisis de inventario usando Google Gemini.
Lee el inventario desde la base de datos (Supabase).
Si la API falla, devuelve un consejo por defecto basado en reglas simples.
"""

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import os
from typing import TypedDict

from google import genai

from database import get_session
from models import Product


# Modelos del diagnóstico (prioridad: gemini-1.5-flash si existiera; luego los que sí aparecieron)
MODELOS_GEMINI = [
    "models/gemini-1.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-2.5-flash",
    "models/gemini-flash-latest",
    "models/gemini-pro-latest",
]

# Umbral bajo para considerar "poco stock"
UMBRAL_STOCK_BAJO = 10


class Producto(TypedDict):
    """Representa un producto del inventario."""

    product_id: str
    product_name: str
    quantity: int


def _obtener_productos_desde_db() -> list[Producto]:
    """
    Abre una sesión nueva, consulta la tabla products y devuelve los datos actuales.
    Sin caché: cada llamada lee de Supabase.
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
    finally:
        session.close()


def _consejo_por_defecto(productos: list[Producto]) -> str:
    """
    Genera un consejo simple basado en reglas (sin IA) para no romper la app.
    """
    en_cero = [p for p in productos if p["quantity"] == 0]
    bajos = [p for p in productos if 0 < p["quantity"] <= UMBRAL_STOCK_BAJO]

    partes: list[str] = []
    if en_cero:
        nombres = ", ".join(p["product_name"] for p in en_cero)
        partes.append(f"Stock en cero: {nombres}. Reabastecer pronto.")
    if bajos:
        nombres = ", ".join(p["product_name"] for p in bajos[:3])
        if len(bajos) > 3:
            nombres += f" y {len(bajos) - 3} más"
        partes.append(f"Poco stock (≤{UMBRAL_STOCK_BAJO}): {nombres}. Considera pedir más.")
    if not partes:
        return "El inventario está en niveles normales. Revisa de nuevo en unos días."

    return " ".join(partes)


def _formatear_inventario(productos: list[Producto]) -> str:
    """Formatea la lista de productos para el prompt de Gemini."""
    return "\n".join(
        f"- {p['product_name']} (id: {p['product_id']}): {p['quantity']} unidades"
        for p in productos
    )


def generar_consejo_inventario() -> str:
    """
    Analiza el inventario (desde la base de datos) con Gemini y devuelve un consejo.
    Si la API falla, devuelve un consejo por defecto basado en reglas simples.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError(
            "GEMINI_API_KEY no está definida. Configúrala en el archivo .env"
        )

    # Consulta fresca a la DB justo antes de enviar a Gemini (sin usar CSV ni caché)
    productos = _obtener_productos_desde_db()
    print("[ai_service] Productos leidos de la DB:", productos)  # noqa: T201

    prompt = f"""Eres un asesor de inventario para una tienda de barrio. 
Analiza este inventario y da UN solo consejo breve y práctico para el dueño (por ejemplo: qué reponer, qué producto tiene alta rotación, qué está por acabarse).
Sé directo, en español y en tono cercano (como para "mi papá").

Inventario (product_id, product_name, quantity):
{_formatear_inventario(productos)}

Responde solo con el consejo, sin títulos ni explicaciones extra."""

    try:
        client = genai.Client(api_key=api_key)
        for model_name in MODELOS_GEMINI:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response.text and response.text.strip():
                    return response.text.strip()
            except Exception as e:
                print(f"[Gemini] Error con modelo '{model_name}': {e!s}")  # noqa: T201
                continue
    except Exception as e:
        print(f"[Gemini] Error de cliente: {e!s}")  # noqa: T201

    # Fallback robusto: consejo por reglas para que la app no se rompa
    return _consejo_por_defecto(productos)
