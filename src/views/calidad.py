import streamlit as st

from ..queries import get_quality_stats
from ..styles import section


def render(data, k):
    q = get_quality_stats()
    section("Calidad y preparación de datos",
            "Esta vista permite demostrar dominio técnico durante la sustentación.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", f"{q['total']:,}")
    c2.metric("Variables originales", "20")
    c3.metric("IDs duplicados", f"{q['duplicated_ids']:,}")
    c4.metric("Nulos satisfacción", f"{q['nulls_satisfaction']:,}")

    st.markdown("### Tratamientos realizados")
    st.markdown("""
    - `fecha_venta` se convirtió a tipo fecha.
    - Se crearon año, mes y trimestre.
    - Se calculó `margen_estimado_cop = precio_venta_cop - costo_estimado_cop`.
    - Se calculó `margen_estimado_pct = margen_estimado_cop / precio_venta_cop`.
    - Se creó una bandera numérica para financiación.
    - Se agruparon los días de entrega en 0-2, 3-4, 5-7 y 8+ días.
    - Los faltantes de satisfacción no se imputaron; se conservan como nulos.
    """)

    st.dataframe(q["missing"], use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Descargar datos filtrados",
        data=data.to_csv(index=False).encode("utf-8-sig"),
        file_name="motocicletas_filtro_dashboard.csv",
        mime="text/csv",
    )
