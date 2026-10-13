"""
Tests del ejercicio ej3f1.py: registro y configuración del panel de administración.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import pytest
from django.contrib import admin

from ej3f1 import Articulo, ArticuloAdmin, Categoria, CategoriaAdmin, sitio


def test_modelos_registrados():
    """Ambos modelos están registrados en el sitio de administración"""
    assert Categoria in sitio._registry, "Categoria debe registrarse en el sitio 'sitio'."
    assert Articulo in sitio._registry, "Articulo debe registrarse en el sitio 'sitio'."


def test_las_clases_admin_heredan_de_modeladmin():
    """Las configuraciones son clases ModelAdmin"""
    assert issubclass(CategoriaAdmin, admin.ModelAdmin)
    assert issubclass(ArticuloAdmin, admin.ModelAdmin)


def test_admin_asociado_a_cada_modelo():
    """Cada modelo usa su propia clase de configuración"""
    assert isinstance(sitio._registry[Categoria], CategoriaAdmin)
    assert isinstance(sitio._registry[Articulo], ArticuloAdmin)


def test_configuracion_de_categoria():
    """La lista de categorías muestra el nombre y si está activa"""
    configuracion = sitio._registry[Categoria]

    assert tuple(configuracion.list_display) == ("nombre", "activa")
    assert tuple(configuracion.search_fields) == ("nombre",)


def test_columnas_de_la_lista_de_articulos():
    """La lista de artículos muestra las columnas pedidas"""
    configuracion = sitio._registry[Articulo]

    assert tuple(configuracion.list_display) == ("nombre", "categoria", "precio", "stock"), (
        "list_display debe ser ('nombre', 'categoria', 'precio', 'stock')."
    )


def test_filtros_y_busqueda_de_articulos():
    """La lista de artículos permite filtrar y buscar"""
    configuracion = sitio._registry[Articulo]

    assert tuple(configuracion.list_filter) == ("categoria", "disponible")
    assert tuple(configuracion.search_fields) == ("nombre", "descripcion")


def test_ordenacion_y_paginacion_de_articulos():
    """La lista de artículos está ordenada y paginada"""
    configuracion = sitio._registry[Articulo]

    assert tuple(configuracion.ordering) == ("nombre",)
    assert configuracion.list_per_page == 25


def test_configuracion_valida():
    """Django no detecta errores en la configuración del panel"""
    errores = sitio._registry[Articulo].check()

    assert errores == [], f"La configuración del panel tiene errores: {errores}"
