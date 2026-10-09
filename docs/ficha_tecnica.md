# Ficha técnica — Fabricante de motocicletas

## 1. Contexto
Fabricante nacional de motocicletas.

## 2. Audiencia
Gerencia comercial y red de concesionarios.

## 3. Problema
Identificar oportunidades de crecimiento rentable y mejora de la experiencia del cliente por
región, canal y segmento.

## 4. Unidad de observación
Una fila representa una venta individual, identificada por `id_venta`.

## 5. Datos
- 55.000 registros.
- 20 variables originales.
- Periodo: 2024-01-01 a 2026-09-30.
- Variables numéricas, categóricas, temporales y geográficas.

## 6. Calidad
- IDs duplicados: 0.
- Faltantes relevantes: 989 en satisfacción postventa.
- Los faltantes de satisfacción no se imputan.

## 7. Variables derivadas
- Año, mes y trimestre.
- `margen_estimado_cop = precio_venta_cop - costo_estimado_cop`.
- `margen_estimado_pct = margen_estimado_cop / precio_venta_cop * 100`.
- `financiado_flag`.
- `entrega_categoria`.

## 8. KPI
**Ventas:** `COUNT(id_venta)`

**Ingresos:** `SUM(precio_venta_cop)`

**Margen estimado:** `SUM(precio_venta_cop - costo_estimado_cop)`

**Margen %:** `SUM(margen_estimado_cop) / SUM(precio_venta_cop) * 100`

**Financiación:** `SUM(financiado_flag) / COUNT(id_venta) * 100`

**Entrega promedio:** `MEAN(dias_entrega)`

**Satisfacción:** `MEAN(satisfaccion_postventa_1a5)`, ignorando nulos.

## 9. Modelo lógico
Se utiliza una tabla transaccional única porque cada registro corresponde a una venta. Las
dimensiones analíticas se encuentran como atributos de la venta: fecha, geografía, producto,
canal, cliente, financiación y forma de pago.

## 10. Tratamiento de faltantes
No se imputa satisfacción porque no existe evidencia para conocer el valor real de una valoración
faltante. Se mantiene el nulo y se excluye únicamente de métricas que requieren satisfacción.

## 11. Limitaciones
El dataset es académico/sintético y no permite afirmar causalidad. En particular, la relación
entre entrega y satisfacción debe presentarse como asociación observada.

## 12. Diseño visual
La página inicial sigue una composición Z/F:
- KPI arriba.
- Evidencia visual en el centro.
- Segmentación después.
- Tabla de detalle al final.
- Filtros en la barra lateral.

La finalidad es que la gerencia pueda pasar de **resultado → explicación → detalle → decisión**.
