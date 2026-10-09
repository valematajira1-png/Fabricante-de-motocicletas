# Guion de sustentación — versión alineada con el dashboard

## 1. Contexto
“Analizamos un fabricante nacional de motocicletas. Nuestro dashboard está dirigido a la gerencia
comercial y la red de concesionarios. Buscamos identificar oportunidades de crecimiento rentable
sin descuidar la experiencia del cliente.”

## 2. Problema
“Queremos responder dónde están las oportunidades de crecimiento rentable y mejora de experiencia
por región, canal y segmento.”

## 3. Preparación
“Trabajamos con 55.000 ventas. Cada registro corresponde a una venta. Creamos variables temporales,
margen estimado, margen porcentual, indicador de financiación y categorías de tiempo de entrega.
Encontramos 989 faltantes en satisfacción y decidimos no imputarlos.”

## 4. Explicación del diseño
“Organizamos la página principal con una lectura Z/F. Arriba están los KPI porque resumen el estado
del negocio. Después aparecen los gráficos que explican esos resultados. Más abajo aparece el
detalle tabular. Los filtros quedan a la izquierda para que la exploración no compita con la
jerarquía visual.”

## 5. Recorrido
### Resumen ejecutivo
1. Mostrar KPI.
2. Cambiar región.
3. Observar cómo cambian los KPI.
4. Mostrar evolución mensual.
5. Comparar regiones.
6. Comparar segmentos y canales.
7. Bajar a la tabla.

### Rentabilidad
1. Mostrar ticket y margen.
2. Comparar margen % por región.
3. Mostrar volumen vs margen por canal.
4. Revisar financiación.

### Experiencia
1. Mostrar días de entrega.
2. Mostrar satisfacción.
3. Analizar entrega vs satisfacción.
4. Filtrar una región.

### Hallazgos
Pasar de dato a decisión:
**Hallazgo → Evidencia → Acción.**

### Calidad
Mostrar faltantes, duplicados y variables derivadas.

## 6. Preguntas técnicas probables

### ¿Por qué no imputaron los nulos de satisfacción?
Porque una valoración faltante no tiene un valor conocido y una imputación introduciría información
no observada. Se excluyen solo de los indicadores que requieren satisfacción.

### ¿Cómo calcularon el margen?
Precio de venta menos costo estimado.

### ¿Por qué margen porcentual total?
Porque se calcula sobre el total de ingresos y representa el margen económico agregado.

### ¿Por qué Streamlit?
Porque permite integrar Python, preparación de datos, cálculos y visualización interactiva en una
aplicación que puede demostrarse durante la sustentación.

### ¿Por qué una línea para ingresos?
Porque la pregunta requiere observar evolución temporal.

### ¿Por qué barras para región?
Porque permiten comparar magnitudes entre categorías.

### ¿Por qué dispersión para entrega y satisfacción?
Porque ambas son variables numéricas y queremos observar una posible relación.

### ¿La entrega causa menor satisfacción?
No. El dashboard muestra una asociación/correlación observada; no permite afirmar causalidad.

### ¿Qué aporta la interacción?
Permite pasar de una visión general a una región, segmento o canal específico y comprobar si el
hallazgo se mantiene o cambia.

## 7. Cierre
“El dashboard transforma 55.000 registros transaccionales en una herramienta para priorizar tres
frentes: crecimiento rentable, gestión de financiación y mejora de tiempos de entrega asociados con
la experiencia del cliente.”
