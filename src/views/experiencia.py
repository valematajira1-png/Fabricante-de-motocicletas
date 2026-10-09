import pandas as pd
import plotly.express as px
import streamlit as st

from ..charts import chart_config
from ..metrics import pct
from ..styles import section


def render(data, k):
    section("Experiencia del cliente",
            "Pregunta: ¿dónde los tiempos de entrega pueden estar acompañando una peor experiencia?")

    c1, c2, c3 = st.columns(3)
    c1.metric("Entrega promedio", f"{k.delivery:.1f} días")
    c2.metric("Satisfacción promedio",
              f"{k.satisfaction:.2f}/5" if not pd.isna(k.satisfaction) else "N/D")
    c3.metric("Cobertura de satisfacción",
              pct(data["satisfaccion_postventa_1a5"].notna().mean() * 100))

    col1, col2 = st.columns(2)
    with col1:
        dist = (data.groupby("entrega_categoria").agg(ventas=("id_venta", "count")).reset_index())
        fig = px.bar(dist, x="entrega_categoria", y="ventas",
                     title="Distribución por tiempo de entrega",
                     labels={"entrega_categoria": "Tiempo de entrega", "ventas": "Ventas"})
        st.plotly_chart(chart_config(fig), use_container_width=True)
    with col2:
        sat = data.groupby("region", as_index=False).agg(
            entrega=("dias_entrega", "mean"),
            satisfaccion=("satisfaccion_postventa_1a5", "mean"),
            ventas=("id_venta", "count"))
        fig = px.scatter(sat, x="entrega", y="satisfaccion", size="ventas",
                         color="region", hover_name="region",
                         title="Entrega vs. satisfacción por región",
                         labels={"entrega": "Días de entrega promedio",
                                 "satisfaccion": "Satisfacción promedio"})
        st.plotly_chart(chart_config(fig).update_layout(hovermode=False), use_container_width=True)

    st.markdown("### Detalle de experiencia")
    exp = (data.groupby("canal_venta", as_index=False).agg(
        ventas=("id_venta", "count"),
        entrega=("dias_entrega", "mean"),
        satisfaccion=("satisfaccion_postventa_1a5", "mean")).sort_values("satisfaccion"))
    st.dataframe(
        exp.style.format({"ventas": "{:,.0f}", "entrega": "{:.1f}", "satisfaccion": "{:.2f}"}),
        use_container_width=True, hide_index=True,
    )

    corr = data[["dias_entrega", "satisfaccion_postventa_1a5"]].corr().iloc[0, 1]
    st.info(
        f"En la selección actual, la correlación entre días de entrega y satisfacción es {corr:.2f}. "
        "Esto representa una asociación observada y no demuestra causalidad."
    )
