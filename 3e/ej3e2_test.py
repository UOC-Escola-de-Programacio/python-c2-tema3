"""
Tests del ejercicio ej3e2.py: jerarquía de plantillas e inclusión de fragmentos.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import re
from pathlib import Path

import pytest

from ej3e2 import renderizar_articulo

PLANTILLAS = Path(__file__).resolve().parent / "templates" / "ej3e2"


def leer(nombre):
    """Devuelve el código fuente de una plantilla del ejercicio"""
    ruta = PLANTILLAS / nombre
    assert ruta.exists(), f"Falta la plantilla '{nombre}'."
    return ruta.read_text(encoding="utf-8")


@pytest.fixture
def entrada():
    """Entrada de blog de ejemplo"""
    return {
        "titulo": "Primeros pasos con Django",
        "texto": "Django es un framework web escrito en Python.",
        "etiquetas": ["python", "django", "web"],
    }


@pytest.fixture
def html(entrada):
    """HTML resultante de renderizar la entrada"""
    return renderizar_articulo(entrada)


def test_jerarquia_de_plantillas():
    """Cada plantilla extiende la del nivel anterior"""
    assert '{% extends "ej3e2/base.html" %}' in leer("base_blog.html"), (
        "'base_blog.html' debe extender 'base.html'."
    )
    assert '{% extends "ej3e2/base_blog.html" %}' in leer("articulo.html"), (
        "'articulo.html' debe extender 'base_blog.html'."
    )


def test_contenido_del_primer_nivel(html):
    """El menú definido en la plantilla base aparece en la página final"""
    assert '<nav class="menu">Inicio</nav>' in html, (
        "El menú de 'base.html' debe heredarse hasta la plantilla final."
    )


def test_contenido_del_segundo_nivel(html):
    """La plantilla de sección aporta el lateral y el contenedor del artículo"""
    assert '<aside class="lateral">' in html and "Últimas entradas" in html, (
        "El bloque 'lateral' debe definirse en 'base_blog.html'."
    )
    assert '<article class="entrada">' in html, (
        "'base_blog.html' debe envolver el contenido en <article class=\"entrada\">."
    )


def test_contenido_del_tercer_nivel(html):
    """La plantilla concreta rellena el bloque 'cuerpo'"""
    titular = re.search(r'<h2 class="titular">(.*?)</h2>', html, re.DOTALL)
    texto = re.search(r'<p class="texto">(.*?)</p>', html, re.DOTALL)

    assert titular is not None, 'Falta el <h2 class="titular">.'
    assert titular.group(1).strip() == "Primeros pasos con Django"
    assert texto is not None, 'Falta el <p class="texto">.'
    assert texto.group(1).strip() == "Django es un framework web escrito en Python."


def test_titulo_de_la_pagina(html):
    """El título de la página es el de la entrada"""
    titulo = re.search(r"<title>(.*?)</title>", html, re.DOTALL)

    assert titulo is not None, "Falta el <title>."
    assert titulo.group(1).strip() == "Primeros pasos con Django", (
        "La plantilla final debe sobrescribir el bloque 'titulo'."
    )


def test_fragmento_incluido(html):
    """Las etiquetas se muestran desde el fragmento incluido"""
    assert '<ul class="etiquetas">' in html, "Debe incluirse el fragmento '_etiquetas.html'."
    etiquetas = re.findall(r"<li>(.*?)</li>", html, re.DOTALL)
    assert [etiqueta.strip() for etiqueta in etiquetas] == ["python", "django", "web"]


def test_se_usa_include_con_with():
    """El fragmento recibe las etiquetas mediante 'with'"""
    articulo = leer("articulo.html")

    assert "{% include" in articulo, "Debe usarse la etiqueta {% include %}."
    assert "etiquetas=entrada.etiquetas" in articulo, (
        "El fragmento debe recibir las etiquetas con 'with etiquetas=entrada.etiquetas'."
    )


def test_entrada_sin_etiquetas(entrada):
    """Una entrada sin etiquetas no genera elementos de lista"""
    entrada["etiquetas"] = []

    html = renderizar_articulo(entrada)

    assert '<ul class="etiquetas">' in html
    assert re.findall(r"<li>(.*?)</li>", html, re.DOTALL) == []
