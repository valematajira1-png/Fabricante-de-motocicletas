"""Carga de datos a la base de datos. No depende de Streamlit (se puede usar desde scripts)."""
import pandas as pd
from sqlalchemy import Date, inspect, text

from .config import CSV_PATH, INDEXED_COLUMNS, TABLE


def load_csv_to_db(engine, csv_path=CSV_PATH, if_exists="replace"):
    """Lee el CSV procesado y lo escribe en la tabla `ventas`.

    if_exists: "replace" (recrea la tabla) o "append" (agrega filas nuevas).
    """
    df = pd.read_csv(csv_path, parse_dates=["fecha_venta"], encoding="utf-8-sig")
    df["fecha_venta"] = df["fecha_venta"].dt.date  # fecha real, sin hora
    df.to_sql(
        TABLE,
        engine,
        if_exists=if_exists,
        index=False,
        chunksize=5000,
        dtype={"fecha_venta": Date()},
    )
    create_indexes(engine)
    return len(df)


def create_indexes(engine):
    with engine.begin() as conn:
        for col in INDEXED_COLUMNS:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS ix_{TABLE}_{col} ON {TABLE} ({col})"))


def table_has_data(engine) -> bool:
    if not inspect(engine).has_table(TABLE):
        return False
    with engine.connect() as conn:
        return conn.execute(text(f"SELECT COUNT(*) FROM {TABLE}")).scalar() > 0
