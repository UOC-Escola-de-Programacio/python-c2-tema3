"""
Tests del ejercicio ej3f2.py: personalización avanzada del panel de administración.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

from decimal import Decimal

import pytest
from django.test import RequestFactory

from ejercicios.config import tablas

from ej3f2 import Producto, ProductoAdmin, sitio


@pytest.fixture
def configuracion():
    """Configuración registrada para el modelo Producto"""
    return sitio._registry[Producto]


@pytest.fixture
def productos():
    """Crea las tablas y varios productos de ejemplo"""
    with tablas(Producto):
        Producto.objects.create(nombre="Teclado", sku="TEC-1", precio=Decimal("25.50"), stock=40)
        Producto.objects.create(nombre="Monitor", sku="MON-1", precio=Decimal("180.00"), stock=4)
        Producto.objects.create(nombre="Ratón", sku="RAT-1", precio=Decimal("15.00"), stock=0)
        yield


def test_modelo_registrado():
    """El producto está registrado con su configuración"""
    assert Producto in sitio._registry
    assert isinstance(sitio._registry[Producto], ProductoAdmin)


def test_columnas_del_listado(configuracion):
    """El listado incluye la columna calculada"""
    assert tuple(configuracion.list_display) == ("nombre", "sku", "precio", "estado_stock")


def test_campos_de_solo_lectura(configuracion):
    """La fecha de creación no se puede editar"""
    assert tuple(configuracion.readonly_fields) == ("creado",)


def test_secciones_del_formulario(configuracion):
    """El formulario se organiza en tres secciones"""
    fieldsets = configuracion.fieldsets

    assert fieldsets is not None, "Debe definirse el atributo 'fieldsets'."
    assert [nombre for nombre, _ in fieldsets] == [
        "Información básica",
        "Inventario",
        "Metadatos",
    ]
    assert tuple(fieldsets[0][1]["fields"]) == ("nombre", "sku")
    assert tuple(fieldsets[1][1]["fields"]) == ("precio", "stock", "agotado")
    assert tuple(fieldsets[2][1]["fields"]) == ("creado",)
    assert "collapse" in fieldsets[2][1].get("classes", ()), (
        "La sección 'Metadatos' debe poder plegarse con la clase CSS 'collapse'."
    )


def test_estado_stock(configuracion, productos):
    """La columna calculada resume el estado del stock"""
    teclado = Producto.objects.get(sku="TEC-1")
    monitor = Producto.objects.get(sku="MON-1")
    raton = Producto.objects.get(sku="RAT-1")

    assert configuracion.estado_stock(teclado) == "Stock suficiente"
    assert configuracion.estado_stock(monitor) == "Stock bajo"
    assert configuracion.estado_stock(raton) == "Sin stock"


def test_titulo_de_la_columna_calculada(configuracion):
    """La columna calculada tiene un título legible"""
    assert getattr(configuracion.estado_stock, "short_description", None) == "Estado", (
        "Debe usarse @admin.display(description='Estado')."
    )


def test_accion_registrada(configuracion):
    """La acción masiva está disponible en el panel"""
    assert "marcar_como_agotado" in configuracion.actions
    assert (
        getattr(configuracion.marcar_como_agotado, "short_description", None)
        == "Marcar como agotado"
    ), "Debe usarse @admin.action(description='Marcar como agotado')."


def test_accion_marcar_como_agotado(configuracion, productos):
    """La acción deja sin stock los productos seleccionados"""
    peticion = RequestFactory().post("/admin/")
    seleccion = Producto.objects.filter(sku__in=["TEC-1", "MON-1"])

    configuracion.marcar_como_agotado(peticion, seleccion)

    for sku in ("TEC-1", "MON-1"):
        producto = Producto.objects.get(sku=sku)
        assert producto.agotado is True, "Los productos seleccionados quedan agotados."
        assert producto.stock == 0, "El stock de los productos seleccionados se pone a 0."

    no_seleccionado = Producto.objects.get(sku="RAT-1")
    assert no_seleccionado.agotado is False, (
        "Los productos no seleccionados no deben modificarse."
    )


def test_configuracion_valida(configuracion):
    """Django no detecta errores en la configuración del panel"""
    errores = configuracion.check()

    assert errores == [], f"La configuración del panel tiene errores: {errores}"
