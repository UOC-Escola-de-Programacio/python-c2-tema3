"""
Enunciado:
Django incluye un panel de administración que genera automáticamente una interfaz
web para gestionar los modelos registrados. Para personalizarla se crea una clase
que hereda de `admin.ModelAdmin` y se registra junto al modelo, normalmente con el
decorador `@admin.register()`.

En este ejercicio configurarás el panel de administración de una tienda. Para no
interferir con el panel por defecto, los modelos se registran en el sitio de
administración `sitio` que ya está creado.

Debes implementar:

1. `CategoriaAdmin`, registrada para el modelo `Categoria` en `sitio`, con:
   - `list_display` = ("nombre", "activa")
   - `search_fields` = ("nombre",)
2. `ArticuloAdmin`, registrada para el modelo `Articulo` en `sitio`, con:
   - `list_display` = ("nombre", "categoria", "precio", "stock")
   - `list_filter` = ("categoria", "disponible")
   - `search_fields` = ("nombre", "descripcion")
   - `ordering` = ("nombre",)
   - `list_per_page` = 25

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3f1_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.contrib import admin  # noqa: E402
from django.db import models  # noqa: E402

# Sitio de administración propio de este ejercicio. En un proyecto real
# registrarías los modelos en 'admin.site' desde el fichero 'admin.py'.
sitio = admin.AdminSite(name="tienda")


class Categoria(models.Model):
    """Categoría de artículos."""

    nombre = models.CharField(max_length=60)
    activa = models.BooleanField(default=True)

    class Meta:
        app_label = "ejercicios"
        ordering = ["nombre"]
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    """Artículo a la venta."""

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="articulos")

    class Meta:
        app_label = "ejercicios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# TODO: Registra esta clase para el modelo Categoria en `sitio` con @admin.register()
class CategoriaAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para las categorías."""

    # TODO: Define list_display y search_fields


# TODO: Registra esta clase para el modelo Articulo en `sitio` con @admin.register()
class ArticuloAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para los artículos."""

    # TODO: Define list_display, list_filter, search_fields, ordering y list_per_page
