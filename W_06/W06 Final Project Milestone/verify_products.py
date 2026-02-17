"""
Script de verificación: cuenta los productos en Supabase e imprime confirmación.
"""

from database import get_session
from models import Product


def main() -> None:
    session = get_session()
    try:
        total = session.query(Product).count()
        print(f"OK Verificacion exitosa: se subieron {total} productos a Supabase.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
