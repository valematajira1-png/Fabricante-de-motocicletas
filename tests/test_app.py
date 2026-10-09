"""Prueba de humo: cada página carga sin errores. Ejecutar con: pytest -q"""
import pytest
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")

PAGES = ["Resumen ejecutivo", "Rentabilidad comercial", "Experiencia del cliente",
         "Hallazgos y decisiones", "Calidad de datos"]


@pytest.mark.parametrize("page", PAGES)
def test_pagina(page):
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception
    at.radio[0].set_value(page).run()
    assert not at.exception, at.exception
    assert not at.error


def test_filtro_region():
    at = AppTest.from_file(APP, default_timeout=60).run()
    first = at.sidebar.multiselect[0]
    first.set_value(first.options[:1]).run()
    assert not at.exception
