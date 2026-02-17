"""
Script de migración: lee inventory.csv e inserta los productos en Supabase.
Evita duplicados por product_id.
Ejecutar una vez después de configurar DATABASE_URL en .env.
"""

import csv
from pathlib import Path

from database import Base, engine, get_session
from models import Product


def migrate_csv_to_cloud(csv_path: str | Path | None = None) -> tuple[int, int]:
    """
    Crea la tabla si no existe, lee el CSV e inserta filas que no existan por product_id.

    Returns:
        (insertados, omitidos_duplicados)
    """
    if csv_path is None:
        csv_path = Path(__file__).resolve().parent / "inventory.csv"

    Base.metadata.create_all(bind=engine)

    session = get_session()
    insertados = 0
    omitidos = 0

    try:
        with open(csv_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_id = (row.get("product_id") or "").strip()
                name = (row.get("product_name") or "").strip()
                try:
                    quantity = int(row.get("quantity", 0))
                except (TypeError, ValueError):
                    quantity = 0

                if not product_id:
                    continue

                existing = session.query(Product).filter(Product.product_id == product_id).first()
                if existing:
                    omitidos += 1
                    continue

                session.add(
                    Product(product_id=product_id, name=name, quantity=quantity)
                )
                insertados += 1

        session.commit()
    finally:
        session.close()

    return insertados, omitidos


if __name__ == "__main__":
    print("Migrando inventory.csv a Supabase...")
    try:
        ins, omit = migrate_csv_to_cloud()
        print(f"Listo. Insertados: {ins}, ya existían (omitidos): {omit}")
    except Exception as e:
        print(f"Error: {e}")
        raise
