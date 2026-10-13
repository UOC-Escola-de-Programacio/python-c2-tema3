"""
Tests del ejercicio ej3e1.py: herencia de plantillas en Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import re

from django.template.loader import render_to_string

from ej3e1 import renderizar_contacto, renderizar_inicio


def contenido(html, patron, mensaje):
    """Devuelve el texto capturado por el patrón indicado"""
    encontrado = re.search(patron, html, re.DOTALL)
    assert encontrado is not None, mensaje
    return encontrado.group(1).strip()


def test_plantilla_base():
    """La plantilla base define los valores por defecto de los bloques"""
    html = render_to_string("ej3e1/base.html")

    assert contenido(html, r"<title>(.*?)</title>", "Falta el <title> en la plantilla base.") == (
        "Escuela de Programación"
    )
    assert contenido(
        html, r'<footer class="pie">(.*?)</footer>', "Falta el <footer> en la plantilla base."
    ) == "Todos los derechos reservados"


def test_inicio_hereda_de_la_base():
    """La página de inicio reutiliza la cabecera de la plantilla base"""
    html = renderizar_inicio("Ana")

    assert '<h1 class="marca">Escuela de Programación</h1>' in html, (
        "'inicio.html' debe extender 'base.html' para heredar la cabecera."
    )


def test_inicio_sobrescribe_el_titulo():
    """La página de inicio define su propio título"""
    html = renderizar_inicio("Ana")

    assert contenido(html, r"<title>(.*?)</title>", "Falta el <title>.") == "Inicio"


def test_inicio_muestra_el_mensaje():
    """El bloque de contenido muestra el nombre recibido"""
    html = renderizar_inicio("Ana")

    assert contenido(
        html, r'<p class="mensaje">(.*?)</p>', 'Falta el <p class="mensaje">.'
    ) == "Hola, Ana"


def test_inicio_mantiene_el_pie_por_defecto():
    """Si la hija no sobrescribe un bloque, se mantiene el del padre"""
    html = renderizar_inicio("Ana")

    assert contenido(html, r'<footer class="pie">(.*?)</footer>', "Falta el <footer>.") == (
        "Todos los derechos reservados"
    )


def test_contacto_sobrescribe_titulo_y_contenido():
    """La página de contacto define su título y su contenido"""
    html = renderizar_contacto("info@example.com")

    assert contenido(html, r"<title>(.*?)</title>", "Falta el <title>.") == "Contacto"
    assert contenido(
        html, r'<p class="email">(.*?)</p>', 'Falta el <p class="email">.'
    ) == "info@example.com"


def test_contacto_amplia_el_pie_con_block_super():
    """El pie de contacto reutiliza el del padre con block.super"""
    html = renderizar_contacto("info@example.com")

    pie = contenido(html, r'<footer class="pie">(.*?)</footer>', "Falta el <footer>.")
    assert pie == "Todos los derechos reservados | Escríbenos", (
        "El bloque 'pie' debe empezar con {{ block.super }} y añadir ' | Escríbenos'."
    )


def test_las_hijas_no_repiten_la_estructura():
    """Las plantillas hijas solo contienen bloques, no la estructura HTML"""
    ruta = __file__.replace("ej3e1_test.py", "templates/ej3e1/inicio.html")
    with open(ruta, encoding="utf-8") as fichero:
        plantilla = fichero.read()

    assert "{% extends" in plantilla, "'inicio.html' debe extender la plantilla base."
    assert "<html" not in plantilla.lower(), (
        "La estructura HTML debe estar únicamente en 'base.html'."
    )
