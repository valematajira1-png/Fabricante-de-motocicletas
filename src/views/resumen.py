import plotly.express as px
import streamlit as st

from ..charts import chart_config
from ..metrics import cop, pct
from ..styles import section


def render(data, k):
    section("Resumen ejecutivo",
            "Lectura Z: primero los indicadores, después la evidencia visual y finalmente el detalle.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Ventas", f"{k.sales:,}")
    c2.metric("Ingresos", cop(k.revenue))
    c3.metric("Margen estimado", cop(k.margin))
    c4.metric("Margen %", pct(k.margin_pct))
    c5.metric("Ventas financiadas", pct(k.financing))

    st.markdown("### 1 · Evolución y desempeño")
    col1, col2 = st.columns(2)
    with col1:
        monthly = data.groupby("mes", as_index=False).agg(ingresos=("precio_venta_cop", "sum"))
        fig = px.line(monthly, x="mes", y="ingresos", markers=True,
                      title="Evolución mensual de ingresos",
                      labels={"mes": "Mes", "ingresos": "Ingresos (COP)"})
        st.plotly_chart(chart_config(fig), use_container_width=True)
    with col2:
        region = (data.groupby("region", as_index=False).agg(ingresos=("precio_venta_cop", "sum"))
                  .sort_values("ingresos", ascending=False))
        fig = px.bar(region, x="ingresos", y="region", orientation="h",
                     title="Ingresos por región",
                     labels={"ingresos": "Ingresos (COP)", "region": ""})
        st.plotly_chart(chart_config(fig), use_container_width=True)

    st.markdown("### 2 · Segmentación comercial")
    col1, col2 = st.columns(2)
    with col1:
        segment = (data.groupby("segmento_moto", as_index=False).agg(ventas=("id_venta", "count"))
                   .sort_values("ventas", ascending=False))
        fig = px.bar(segment, x="segmento_moto", y="ventas",
                     title="Volumen de ventas por segmento",
                     labels={"segmento_moto": "Segmento", "ventas": "Ventas"})
        st.plotly_chart(chart_config(fig), use_container_width=True)
    with col2:
        channel = (data.groupby("canal_venta", as_index=False).agg(ingresos=("precio_venta_cop", "sum"))
                   .sort_values("ingresos", ascending=False))
        fig = px.bar(channel, x="canal_venta", y="ingresos",
                     title="Ingresos por canal",
                     labels={"canal_venta": "Canal", "ingresos": "Ingresos (COP)"})
        st.plotly_chart(chart_config(fig), use_container_width=True)

    st.markdown("### 3 · Detalle para profundizar")
    detail = data.groupby(["region", "canal_venta"], as_index=False).agg(
        ventas=("id_venta", "count"),
        ingresos=("precio_venta_cop", "sum"),
        margen=("margen_estimado_cop", "sum"),
        entrega_promedio=("dias_entrega", "mean"),
        satisfaccion=("satisfaccion_postventa_1a5", "mean"),
    )
    detail["margen_pct"] = detail["margen"] / detail["ingresos"] * 100
    st.dataframe(
        detail.sort_values("ingresos", ascending=False).style.format({
            "ventas": "{:,.0f}", "ingresos": "${:,.0f}", "margen": "${:,.0f}",
            "margen_pct": "{:.1f}%", "entrega_promedio": "{:.1f}", "satisfaccion": "{:.2f}",
        }),
        use_container_width=True, hide_index=True,
    )
