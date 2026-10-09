"""Punto de entrada: configuración, filtros y navegación. La lógica vive en src/."""
import streamlit as st

st.set_page_config(
    page_title="BI | Fabricante de motocicletas",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src import styles
from src.config import FILTER_COLUMNS
from src.metrics import compute_kpis
from src.queries import get_filter_options, get_filtered_data
from src.views import calidad, experiencia, hallazgos, rentabilidad, resumen

# Páginas: para agregar una nueva, crea src/views/<nombre>.py con render(data, k) y regístrala aquí.
PAGES = {
    "Resumen ejecutivo": resumen,
    "Rentabilidad comercial": rentabilidad,
    "Experiencia del cliente": experiencia,
    "Hallazgos y decisiones": hallazgos,
    "Calidad de datos": calidad,
}

styles.apply()

# ---------------- Filtros (barra lateral) ----------------
options = get_filter_options()

st.sidebar.title("🎛️ Filtros de análisis")
st.sidebar.caption("Los filtros modifican simultáneamente KPI, gráficos y tablas.")

date_range = st.sidebar.date_input(
    "Periodo",
    value=(options["min_date"], options["max_date"]),
    min_value=options["min_date"],
    max_value=options["max_date"],
)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = options["min_date"], options["max_date"]

selected = {
    col: st.sidebar.multiselect(label, options[col], default=options[col])
    for col, label in FILTER_COLUMNS.items()
}

if any(len(v) == 0 for v in selected.values()):
    st.error("No hay registros para la combinación de filtros seleccionada.")
    st.stop()

# Solo se envía a SQL un filtro si realmente restringe (no todas las opciones elegidas).
active_filters = tuple(
    (col, tuple(vals)) for col, vals in selected.items() if set(vals) != set(options[col])
)

data = get_filtered_data(start_date, end_date, active_filters)
if data.empty:
    st.error("No hay registros para la combinación de filtros seleccionada.")
    st.stop()

# ---------------- Encabezado y navegación ----------------
st.markdown('<div class="main-title">🏍️ Fabricante de motocicletas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Dashboard de desempeño comercial, rentabilidad y experiencia del cliente</div>',
    unsafe_allow_html=True,
)

page = st.radio("Navegación", list(PAGES), horizontal=True, label_visibility="collapsed")
PAGES[page].render(data, compute_kpis(data))

st.sidebar.divider()
st.sidebar.caption("Proyecto final BI 2026-2 · Streamlit + Python")
st.sidebar.caption("Lectura visual: Z/F · KPI → evidencia → detalle")
