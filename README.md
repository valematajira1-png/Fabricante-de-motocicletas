# Proyecto final BI — Fabricante de motocicletas

Dashboard interactivo en **Streamlit + Python** sobre una **base de datos SQL** (SQLite por defecto,
Postgres con una variable de configuración).

## Estructura

```
app.py                 Entrada: filtros + navegación
src/
  config.py            Rutas, tabla, columnas filtrables
  db.py                Conexión (SQLite local o DATABASE_URL)
  etl.py               CSV -> base de datos (+ índices)
  queries.py           ÚNICO lugar con SQL (filtros, opciones, calidad de datos)
  metrics.py           KPI y formatos
  charts.py, styles.py Estilo compartido
  views/               Una página por archivo
scripts/build_db.py    Cargar/actualizar datos manualmente
tests/test_app.py      Prueba de humo de todas las páginas
data/                  CSV procesado (y original en data/raw)
```

## Ejecutar en local

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

La primera vez, la app crea `data/motocicletas.db` automáticamente desde el CSV (unos segundos).

## Publicar (Streamlit Community Cloud)

1. Sube la carpeta a un repositorio de GitHub (el `.gitignore` ya excluye la `.db`, el entorno virtual y los secretos).
2. En https://share.streamlit.io → **Create app** → elige el repo, rama `main`, archivo `app.py`.
3. **Deploy**. Cada `git push` actualiza la app.

## Escalar

| Necesidad | Qué hacer |
|---|---|
| Datos nuevos | `python scripts/build_db.py --csv nuevo.csv --append` |
| Muchos usuarios / datos que cambian | Usar Postgres (Supabase, Neon): en `requirements.txt` descomenta `psycopg2-binary` y define `DATABASE_URL` en *Settings → Secrets* (ver `.streamlit/secrets.toml.example`). Carga inicial: `DATABASE_URL=... python scripts/build_db.py`. **No hay que cambiar código.** |
| Millones de filas | Los filtros ya se ejecutan en SQL con índices. El siguiente paso es mover las agregaciones de `src/views/` a `GROUP BY` en `src/queries.py`. |
| Nueva página | Crear `src/views/<nombre>.py` con `render(data, k)` y registrarla en `PAGES` (`app.py`). |
| Pruebas | `pip install pytest && pytest -q` |

## Problema de negocio
¿Dónde están las oportunidades de crecimiento rentable y mejora de la experiencia del cliente por región,
canal y segmento de motocicleta? Audiencia: gerencia comercial y red de concesionarios.

## Importante: grupo
La guía entregada contiene una discrepancia: en su tabla de asignación aparece el fabricante de
motocicletas para el grupo 1 y el banco minorista para el grupo 4. Este proyecto usa
`01_fabricante_motocicletas.csv`. Confirma la asignación con el docente antes de la entrega.
