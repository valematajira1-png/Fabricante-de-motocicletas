"""Construye o actualiza la base de datos desde un CSV.

Uso:
    python scripts/build_db.py                      # recrea la BD desde data/motocicletas_procesado.csv
    python scripts/build_db.py --csv nuevo.csv --append   # agrega filas nuevas
    DATABASE_URL=postgresql+psycopg2://... python scripts/build_db.py   # carga a Postgres
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine  # noqa: E402

from src.config import CSV_PATH, DEFAULT_DB_URL  # noqa: E402
from src.etl import load_csv_to_db  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--csv", default=str(CSV_PATH))
parser.add_argument("--append", action="store_true", help="agregar en vez de reemplazar")
args = parser.parse_args()

url = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
n = load_csv_to_db(create_engine(url), args.csv, "append" if args.append else "replace")
print(f"Cargadas {n:,} filas en {url.split('@')[-1]}")
