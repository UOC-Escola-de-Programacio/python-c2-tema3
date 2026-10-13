"""
Tests del ejercicio ej3d2.py: bucles y condicionales en las plantillas de Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import re

import pytest

from ej3d2 import renderizar_tabla


def celdas(html, clase):
    """Devuelve el contenido de todas las celdas con la clase indicada"""
    return [
        texto.strip()
        for texto in re.findall(rf'<td class="{clase}">(.*?)</td>', html, re.DOTALL)
    ]


@pytest.fixture
def productos():
    """Inventario de ejemplo"""
    return [
        {"nombre": "Teclado", "precio": 25.5, "stock": 12},
        {"nombre": "Monitor", "precio": 180.0, "stock": 3},
        {"nombre": "Ratón", "precio": 15.0, "stock": 0},
    ]


def test_una_fila_por_producto(productos):
    """Se genera una fila por cada producto"""
    html = renderizar_tabla(productos)

    assert celdas(html, "nombre") == ["Teclado", "Monitor", "Ratón"], (
        "Debe recorrerse la lista con {% for %}."
    )


def test_numeracion(productos):
    """Las filas se numeran empezando por 1"""
    html = renderizar_tabla(productos)

    assert celdas(html, "numero") == ["1", "2", "3"], "Debe usarse forloop.counter."


def test_precios_formateados(productos):
    """Los precios se muestran con dos decimales"""
    html = renderizar_tabla(productos)

    assert celdas(html, "precio") == ["25.50 €", "180.00 €", "15.00 €"], (
        "Debe usarse el filtro 'floatformat:2' seguido de ' €'."
    )


def test_estado_del_stock(productos):
    """El texto del stock depende de la cantidad disponible"""
    html = renderizar_tabla(productos)

    assert celdas(html, "stock") == ["Disponible", "Últimas unidades", "Sin stock"], (
        "Debe usarse {% if %}, {% elif %} y {% else %} según el stock."
    )


def test_lista_vacia():
    """Con una lista vacía se muestra un mensaje"""
    html = renderizar_tabla([])

    assert '<tr class="vacia">' in html, "Debe usarse la etiqueta {% empty %}."
    assert "No hay productos" in html
    assert celdas(html, "nombre") == [], "No debe generarse ninguna fila de producto."


def test_total_de_productos(productos):
    """Se muestra el número total de productos"""
    html = renderizar_tabla(productos)

    encontrado = re.search(r'<p class="total">(.*?)</p>', html, re.DOTALL)
    assert encontrado is not None, 'Falta el elemento <p class="total">.'
    assert encontrado.group(1).strip() == "Total: 3 productos", (
        "Debe usarse el filtro 'length' para contar los productos."
    )


def test_total_con_lista_vacia():
    """El total también funciona con una lista vacía"""
    html = renderizar_tabla([])

    assert "Total: 0 productos" in html
