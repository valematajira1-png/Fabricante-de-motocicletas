"""Capa de acceso a datos. Toda consulta SQL del dashboard vive aquí.

Si el volumen crece, esta es la única capa que hay que optimizar
(por ejemplo, pasar agregaciones de pandas a GROUP BY en SQL).
"""
from datetime import date

import pandas as pd
import streamlit as st
from sqlalchemy import bindparam, inspect, text

from .config import FILTER_COLUMNS, TABLE
from .db import get_engine


@st.cache_data(ttl=3600, show_spinner=False)
def get_filter_options() -> dict:
    """Valores disponibles para cada filtro y rango de fechas."""
    engine = get_engine()
    options = {}
    with engine.connect() as conn:
        for col in FILTER_COLUMNS:
            rows = conn.execute(
                text(f"SELECT DISTINCT {col} FROM {TABLE} WHERE {col} IS NOT NULL ORDER BY {col}")
            ).scalars().all()
            options[col] = list(rows)
        lo, hi = conn.execute(text(f"SELECT MIN(fecha_venta), MAX(fecha_venta) FROM {TABLE}")).one()
    options["min_date"] = pd.to_datetime(lo).date()
    options["max_date"] = pd.to_datetime(hi).date()
    return options


@st.cache_data(ttl=600, show_spinner="Consultando datos…")
def get_filtered_data(start: date, end: date, filters: tuple) -> pd.DataFrame:
    """Devuelve solo las filas que cumplen los filtros (el filtrado ocurre en SQL).

    `filters` es una tupla de pares (columna, valores). Los filtros con todas las
    opciones seleccionadas no deben incluirse (no restringen nada).
    """
    clauses = ["fecha_venta BETWEEN :start AND :end"]
    params = {"start": start.isoformat(), "end": end.isoformat()}
    bind_params = []
    for i, (col, values) in enumerate(filters):
        if col not in FILTER_COLUMNS:  # lista blanca: evita inyección SQL
            raise ValueError(f"Filtro no permitido: {col}")
        name = f"f{i}"
        clauses.append(f"{col} IN :{name}")
        params[name] = list(values)
        bind_params.append(bindparam(name, expanding=True))

    query = text(f"SELECT * FROM {TABLE} WHERE {' AND '.join(clauses)}").bindparams(*bind_params)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn, params=params, parse_dates=["fecha_venta"])


@st.cache_data(ttl=3600, show_spinner=False)
def get_quality_stats() -> dict:
    """Calidad de datos de la tabla completa, calculada en la base de datos."""
    engine = get_engine()
    cols = [c["name"] for c in inspect(engine).get_columns(TABLE)]
    nulls_sql = ", ".join(f"COUNT(*) - COUNT({c}) AS {c}" for c in cols)
    with engine.connect() as conn:
        total, distinct_ids = conn.execute(
            text(f"SELECT COUNT(*), COUNT(DISTINCT id_venta) FROM {TABLE}")
        ).one()
        nulls = conn.execute(text(f"SELECT {nulls_sql} FROM {TABLE}")).mappings().one()
    missing = (
        pd.DataFrame({"variable": list(nulls.keys()), "faltantes": list(nulls.values())})
        .query("faltantes > 0")
        .sort_values("faltantes", ascending=False)
    )
    return {
        "total": int(total),
        "duplicated_ids": int(total - distinct_ids),
        "nulls_satisfaction": int(nulls.get("satisfaccion_postventa_1a5", 0)),
        "missing": missing,
    }
