"""
Enunciado:
El panel de administración de Django se puede personalizar mucho más allá de las
columnas del listado: se pueden agrupar los campos del formulario en secciones
(`fieldsets`), marcar campos como de solo lectura (`readonly_fields`), añadir
columnas calculadas con métodos decorados con `@admin.display` y definir acciones
masivas con `@admin.action`.

En este ejercicio completarás la clase `ProductoAdmin` para que:

1. Muestre en el listado las columnas ("nombre", "sku", "precio", "estado_stock").
2. Tenga el campo `creado` como solo lectura (`readonly_fields`).
3. Organice el formulario en tres secciones (`fieldsets`):
   - "Información básica" con los campos ("nombre", "sku")
   - "Inventario" con los campos ("precio", "stock", "agotado")
   - "Metadatos" con el campo ("creado",) y la clase CSS "collapse"
4. Defina el método `estado_stock(producto)`, decorado con
   `@admin.display(description="Estado")`, que devuelva:
   - "Sin stock" si el stock es 0,
   - "Stock bajo" si es menor que 10,
   - "Stock suficiente" en el resto de casos.
5. Defina la acción `marcar_como_agotado`, decorada con
   `@admin.action(description="Marcar como agotado")`, que ponga `agotado=True` y
   `stock=0` en todos los productos seleccionados, y la registre en `actions`.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3f2_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.contrib import admin  # noqa: E402
from django.db import models  # noqa: E402

# Sitio de administración propio de este ejercicio.
sitio = admin.AdminSite(name="inventario")


class Producto(models.Model):
    """Producto del inventario."""

    nombre = models.CharField(max_length=120)
    sku = models.CharField(max_length=20, unique=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    agotado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "ejercicios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


@admin.register(Producto, site=sitio)
class ProductoAdmin(admin.ModelAdmin):
    """Configuración avanzada del panel de administración de productos."""

    # TODO: Define list_display, readonly_fields, fieldsets y actions

    # TODO: Define el método estado_stock(), decorado con
    # @admin.display(description="Estado")

    # TODO: Define la acción marcar_como_agotado(), decorada con
    # @admin.action(description="Marcar como agotado")
