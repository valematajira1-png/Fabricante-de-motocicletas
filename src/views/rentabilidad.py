import plotly.express as px
import streamlit as st

from ..charts import chart_config
from ..metrics import cop, pct
from ..styles import section


def render(data, k):
    section("Rentabilidad comercial",
            "Pregunta: ¿dónde se concentra el volumen y dónde se obtiene la mejor rentabilidad relativa?")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ticket promedio", cop(data["precio_venta_cop"].mean()))
    c2.metric("Margen promedio / venta", cop(data["margen_estimado_cop"].mean()))
    c3.metric("Descuento promedio", pct(data["descuento_pct"].mean()))
    c4.metric("Financiación", pct(k.financing))

    col1, col2 = st.columns(2)
    with col1:
        reg = data.groupby("region", as_index=False).agg(
            ingresos=("precio_venta_cop", "sum"), margen=("margen_estimado_cop", "sum"))
        reg["margen_pct"] = reg["margen"] / reg["ingresos"] * 100
        reg = reg.sort_values("margen_pct", ascending=False)
        fig = px.bar(reg, x="margen_pct", y="region", orientation="h",
                     title="Margen estimado % por región",
                     labels={"margen_pct": "Margen %", "region": ""})
        st.plotly_chart(chart_config(fig), use_container_width=True)
    with col2:
        ch = data.groupby("canal_venta", as_index=False).agg(
            ventas=("id_venta", "count"),
            ingresos=("precio_venta_cop", "sum"),
            margen=("margen_estimado_cop", "sum"))
        ch["margen_pct"] = ch["margen"] / ch["ingresos"] * 100
        fig = px.scatter(ch, x="ventas", y="margen_pct", size="ingresos",
                         color="canal_venta", hover_name="canal_venta",
                         title="Volumen vs. margen por canal",
                         labels={"ventas": "Ventas", "margen_pct": "Margen %"})
        st.plotly_chart(chart_config(fig).update_layout(hovermode=False), use_container_width=True)

    st.markdown("### Financiación")
    ft = data.groupby("financiado", as_index=False).agg(
        ventas=("id_venta", "count"),
        ingresos=("precio_venta_cop", "sum"),
        ticket=("precio_venta_cop", "mean"),
        plazo_promedio=("plazo_meses", "mean"),
        margen=("margen_estimado_cop", "sum"))
    ft["participacion"] = ft["ventas"] / ft["ventas"].sum() * 100
    st.dataframe(
        ft.style.format({
            "ventas": "{:,.0f}", "ingresos": "${:,.0f}", "ticket": "${:,.0f}",
            "plazo_promedio": "{:.1f}", "margen": "${:,.0f}", "participacion": "{:.1f}%",
        }),
        use_container_width=True, hide_index=True,
    )
