"""Configuración central del proyecto."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "motocicletas_procesado.csv"
SQLITE_PATH = ROOT / "data" / "motocicletas.db"
DEFAULT_DB_URL = f"sqlite:///{SQLITE_PATH.as_posix()}"

TABLE = "ventas"

# Columnas por las que se filtra en la barra lateral (lista blanca: se usan en SQL).
FILTER_COLUMNS = {
    "region": "Región",
    "segmento_moto": "Segmento de moto",
    "canal_venta": "Canal de venta",
    "tipo_cliente": "Tipo de cliente",
}

# Columnas con índice en la base de datos (aceleran los filtros).
INDEXED_COLUMNS = ["fecha_venta", *FILTER_COLUMNS.keys()]
