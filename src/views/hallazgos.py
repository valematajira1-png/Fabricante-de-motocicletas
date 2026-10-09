import pandas as pd
import streamlit as st

from ..metrics import cop, pct
from ..styles import section


def _card(title, body):
    return f'<div class="insight-card"><h4>{title}</h4><p>{body}</p></div>'


def render(data, k):
    section("Hallazgos y decisiones",
            "Convertimos los indicadores en acciones que la gerencia puede priorizar.")

    top_region = data.groupby("region")["precio_venta_cop"].sum().idxmax()
    top_segment = data.groupby("segmento_moto")["id_venta"].count().idxmax()
    top_channel = data.groupby("canal_venta")["precio_venta_cop"].sum().idxmax()
    corr = data[["dias_entrega", "satisfaccion_postventa_1a5"]].corr().iloc[0, 1]

    a, b = st.columns(2)
    a.markdown(_card("📈 Escala comercial",
        f"La selección actual registra <b>{k.sales:,} ventas</b>, <b>{cop(k.revenue)}</b> de ingresos "
        f"y un margen estimado de <b>{pct(k.margin_pct)}</b>."), unsafe_allow_html=True)
    b.markdown(_card("🗺️ Concentración",
        f"La región de mayor ingreso es <b>{top_region}</b>. El segmento con mayor volumen es "
        f"<b>{top_segment}</b> y el canal de mayor ingreso es <b>{top_channel}</b>."), unsafe_allow_html=True)

    st.write("")
    a, b = st.columns(2)
    a.markdown(_card("🚚 Experiencia",
        f"El tiempo promedio de entrega es <b>{k.delivery:.1f} días</b> y la satisfacción promedio "
        f"es <b>{k.satisfaction:.2f}/5</b> cuando existe dato."), unsafe_allow_html=True)
    b.markdown(_card("🔎 Señal de gestión",
        f"La correlación entrega-satisfacción es <b>{corr:.2f}</b>. Es una señal para priorizar "
        "análisis operativo, no una prueba de causalidad."), unsafe_allow_html=True)

    st.markdown("### De hallazgo a decisión")
    decisions = pd.DataFrame({
        "Hallazgo": [
            "Concentración de ingresos por regiones y canales",
            "Segmentos con alto volumen",
            "Casos de entrega de 8+ días",
            "Alta participación de financiación",
        ],
        "Decisión sugerida": [
            "Proteger disponibilidad y nivel de servicio en los mercados de mayor aporte.",
            "Revisar margen y descuentos antes de ampliar promociones.",
            "Priorizar revisión de capacidad logística y promesa de entrega.",
            "Gestionar financiación junto con ticket, volumen y margen.",
        ],
        "Indicador de seguimiento": [
            "Ingresos + margen %", "Ventas + margen %",
            "Días de entrega + satisfacción", "Financiación + margen",
        ],
    })
    st.dataframe(decisions, use_container_width=True, hide_index=True)

    st.markdown("### Las 5 preguntas que responde el dashboard")
    for i, q in enumerate([
        "¿Cómo evolucionan ventas e ingresos?",
        "¿Qué regiones, segmentos y canales concentran el desempeño?",
        "¿Dónde está la mejor combinación de volumen y rentabilidad?",
        "¿Qué papel tiene la financiación en la mezcla comercial?",
        "¿Cómo se relacionan tiempos de entrega y satisfacción?",
    ], 1):
        st.markdown(f"**{i}.** {q}")
