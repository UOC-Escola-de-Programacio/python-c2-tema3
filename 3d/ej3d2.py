"""
Enunciado:
Las plantillas de Django incluyen etiquetas de control de flujo que permiten
recorrer colecciones (`{% for %}`), tratar el caso de una lista vacía
(`{% empty %}`) y tomar decisiones (`{% if %}`, `{% elif %}`, `{% else %}`).
Dentro de un bucle, la variable especial `forloop` ofrece información como
`forloop.counter` (posición empezando en 1).

En este ejercicio debes completar la plantilla 'ej3d2/tabla.html' (en la carpeta
3d/templates/ej3d2/) para mostrar un inventario de productos, y la función
`renderizar_tabla()` que la renderiza.

La plantilla debe generar, dentro de un `<table>`, una fila `<tr>` por producto con:

1. `<td class="numero">`: la posición del producto en la lista, empezando en 1.
2. `<td class="nombre">`: el nombre del producto.
3. `<td class="precio">`: el precio con dos decimales seguido de ` €`.
4. `<td class="stock">`: "Sin stock" si el stock es 0, "Últimas unidades" si es
   menor que 5 y "Disponible" en el resto de casos.

Además:

5. Si la lista está vacía debe generarse una única fila
   `<tr class="vacia"><td>No hay productos</td></tr>` usando `{% empty %}`.
6. Fuera de la tabla debe aparecer `<p class="total">Total: N productos</p>`,
   donde N es el número de productos (filtro `length`).

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3d2_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.template.loader import render_to_string  # noqa: E402


def renderizar_tabla(productos):
    """
    Renderiza la plantilla 'ej3d2/tabla.html' con la lista de productos indicada y
    devuelve el HTML generado.
    """
    # TODO: Renderiza la plantilla y devuelve el HTML
    pass


if __name__ == "__main__":
    productos = [
        {"nombre": "Teclado", "precio": 25.5, "stock": 12},
        {"nombre": "Monitor", "precio": 180.0, "stock": 3},
        {"nombre": "Ratón", "precio": 15.0, "stock": 0},
    ]
    print(renderizar_tabla(productos))
