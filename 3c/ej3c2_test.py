"""
Tests del ejercicio ej3c2.py: consultas con el ORM de Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from ejercicios.config import tablas

from ej3c2 import (
    Cliente,
    Pedido,
    buscar_clientes,
    clientes_de_ciudad,
    nombres_de_clientes,
    pedidos_caros,
    pedidos_pendientes,
    ranking_clientes,
    total_gastado,
)


@pytest.fixture
def datos():
    """Crea las tablas y un conjunto de datos de ejemplo"""
    with tablas(Cliente, Pedido):
        ana = Cliente.objects.create(nombre="Ana", email="ana@correo.com", ciudad="Barcelona")
        luis = Cliente.objects.create(nombre="Luis", email="luis@correo.com", ciudad="Madrid")
        marta = Cliente.objects.create(
            nombre="Marta", email="marta@ejemplo.com", ciudad="barcelona"
        )

        Pedido.objects.create(cliente=ana, producto="Teclado", importe=Decimal("25.50"), pagado=True)
        Pedido.objects.create(cliente=ana, producto="Monitor", importe=Decimal("180.00"))
        Pedido.objects.create(cliente=luis, producto="Ratón", importe=Decimal("15.00"))

        yield {"ana": ana, "luis": luis, "marta": marta}


def test_clientes_de_ciudad(datos):
    """Los clientes se filtran por ciudad sin distinguir mayúsculas"""
    clientes = clientes_de_ciudad("Barcelona")

    assert [cliente.nombre for cliente in clientes] == ["Ana", "Marta"], (
        "Deben devolverse los clientes de Barcelona, ignorando mayúsculas."
    )


def test_clientes_de_ciudad_sin_resultados(datos):
    """Una ciudad sin clientes devuelve un QuerySet vacío"""
    assert clientes_de_ciudad("Sevilla").count() == 0


def test_pedidos_pendientes(datos):
    """Los pedidos no pagados se devuelven del más caro al más barato"""
    pendientes = pedidos_pendientes()

    assert [pedido.producto for pedido in pendientes] == ["Monitor", "Ratón"], (
        "Solo los pedidos no pagados, ordenados por importe descendente."
    )


def test_pedidos_caros(datos):
    """Se filtran los pedidos por importe mínimo"""
    caros = pedidos_caros(Decimal("20.00"))

    assert {pedido.producto for pedido in caros} == {"Teclado", "Monitor"}


def test_pedidos_caros_usa_select_related(datos):
    """select_related evita una consulta adicional por cada cliente"""
    with CaptureQueriesContext(connection) as consultas:
        for pedido in pedidos_caros(Decimal("0")):
            _ = pedido.cliente.nombre

    assert len(consultas) == 1, (
        "Con select_related('cliente') debe bastar una única consulta a la base de datos."
    )


def test_buscar_clientes_por_nombre(datos):
    """La búsqueda encuentra clientes por su nombre"""
    resultados = buscar_clientes("mar")

    assert [cliente.nombre for cliente in resultados] == ["Marta"]


def test_buscar_clientes_por_email(datos):
    """La búsqueda también mira el email"""
    resultados = buscar_clientes("ejemplo.com")

    assert [cliente.nombre for cliente in resultados] == ["Marta"], (
        "Marta es la única con un email de 'ejemplo.com'."
    )


def test_buscar_clientes_combina_ambos_campos(datos):
    """Se devuelven los clientes que coinciden en cualquiera de los dos campos"""
    resultados = buscar_clientes("correo.com")

    assert {cliente.nombre for cliente in resultados} == {"Ana", "Luis"}, (
        "Ana y Luis tienen un email de 'correo.com'."
    )


def test_total_gastado(datos):
    """Se suman los importes de los pedidos del cliente"""
    assert total_gastado(datos["ana"]) == Decimal("205.50")
    assert total_gastado(datos["luis"]) == Decimal("15.00")


def test_total_gastado_sin_pedidos(datos):
    """Un cliente sin pedidos ha gastado 0"""
    assert total_gastado(datos["marta"]) == Decimal("0"), (
        "Sin pedidos, aggregate() devuelve None y debe convertirse en 0."
    )


def test_ranking_clientes(datos):
    """Los clientes se anotan con su número de pedidos"""
    ranking = list(ranking_clientes())

    assert [cliente.nombre for cliente in ranking] == ["Ana", "Luis", "Marta"]
    assert [cliente.num_pedidos for cliente in ranking] == [2, 1, 0], (
        "El atributo anotado debe llamarse 'num_pedidos'."
    )


def test_nombres_de_clientes(datos):
    """values_list devuelve directamente los nombres"""
    nombres = nombres_de_clientes()

    assert nombres == ["Ana", "Luis", "Marta"]
    assert all(isinstance(nombre, str) for nombre in nombres), (
        "Con flat=True se obtiene una lista de cadenas, no de tuplas."
    )
