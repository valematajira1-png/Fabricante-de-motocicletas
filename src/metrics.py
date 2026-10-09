from dataclasses import dataclass

import numpy as np
import pandas as pd


def cop(value) -> str:
    if pd.isna(value):
        return "$0"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f} B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f} M"
    return f"${value:,.0f}"


def pct(value) -> str:
    return f"{value:.1f}%"


@dataclass
class Kpis:
    sales: int
    revenue: float
    margin: float
    margin_pct: float
    financing: float
    delivery: float
    satisfaction: float


def compute_kpis(data: pd.DataFrame) -> Kpis:
    sales = len(data)
    revenue = data["precio_venta_cop"].sum()
    margin = data["margen_estimado_cop"].sum()
    sat = data["satisfaccion_postventa_1a5"]
    return Kpis(
        sales=sales,
        revenue=revenue,
        margin=margin,
        margin_pct=margin / revenue * 100 if revenue else 0,
        financing=data["financiado_flag"].mean() * 100 if sales else 0,
        delivery=data["dias_entrega"].mean() if sales else 0,
        satisfaction=sat.mean() if sat.notna().any() else np.nan,
    )
