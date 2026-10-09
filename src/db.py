"""Conexión a la base de datos (SQLite por defecto, Postgres u otra vía DATABASE_URL)."""
import os

import streamlit as st
from sqlalchemy import create_engine

from .config import DEFAULT_DB_URL
from .etl import load_csv_to_db, table_has_data


def get_database_url() -> str:
    """Orden de prioridad: variable de entorno > st.secrets > SQLite local."""
    url = os.getenv("DATABASE_URL")
    if not url:
        try:
            url = st.secrets.get("DATABASE_URL")
        except Exception:
            url = None
    return url or DEFAULT_DB_URL


@st.cache_resource(show_spinner="Preparando base de datos…")
def get_engine():
    engine = create_engine(get_database_url(), pool_pre_ping=True)
    # Primera ejecución (local o en la nube): si la tabla no existe, se construye desde el CSV.
    if not table_has_data(engine):
        load_csv_to_db(engine)
    return engine
