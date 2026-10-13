"""
Tests del ejercicio ej3d1.py: variables y filtros en las plantillas de Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import re
from datetime import date

import pytest

from ej3d1 import renderizar_ficha


def etiqueta(html, clase):
    """Devuelve el contenido del párrafo con la clase indicada"""
    encontrado = re.search(rf'<p class="{clase}">(.*?)</p>', html, re.DOTALL)
    assert encontrado is not None, f"Falta el elemento <p class=\"{clase}\"> en la plantilla."
    return encontrado.group(1).strip()


@pytest.fixture
def empleado():
    """Empleado de ejemplo"""
    return {
        "nombre": "ana lópez",
        "puesto": "desarrolladora web",
        "salario": 32450.5,
        "fecha_alta": date(2021, 3, 8),
        "telefono": "600 123 456",
        "activo": True,
    }


def test_nombre_capitalizado(empleado):
    """El nombre se muestra capitalizado dentro de un <h1>"""
    html = renderizar_ficha(empleado)

    encontrado = re.search(r"<h1>(.*?)</h1>", html, re.DOTALL)
    assert encontrado is not None, "La ficha debe incluir un elemento <h1>."
    assert encontrado.group(1).strip() == "Ana López", "Debe usarse el filtro 'title'."


def test_puesto_en_mayusculas(empleado):
    """El puesto se muestra en mayúsculas"""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "puesto") == "DESARROLLADORA WEB", "Debe usarse el filtro 'upper'."


def test_salario_con_dos_decimales(empleado):
    """El salario se formatea con dos decimales y el símbolo del euro"""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "salario") == "32450.50 €", (
        "Debe usarse el filtro 'floatformat:2' seguido de ' €'."
    )


def test_fecha_formateada(empleado):
    """La fecha de alta se muestra en formato d/m/Y"""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "alta") == "08/03/2021", 'Debe usarse el filtro date:"d/m/Y".'


def test_telefono(empleado):
    """Si hay teléfono se muestra tal cual"""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "telefono") == "600 123 456"


def test_telefono_vacio(empleado):
    """Si el teléfono está vacío se muestra un valor por defecto"""
    empleado["telefono"] = ""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "telefono") == "No disponible", "Debe usarse el filtro 'default'."


def test_empleado_activo(empleado):
    """El estado depende del valor de 'activo'"""
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "estado") == "Activo"


def test_empleado_inactivo(empleado):
    """Un empleado no activo aparece como inactivo"""
    empleado["activo"] = False
    html = renderizar_ficha(empleado)

    assert etiqueta(html, "estado") == "Inactivo", "Debe usarse {% if %} ... {% else %}."
