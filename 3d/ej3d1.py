"""
Enunciado:
Las plantillas de Django combinan HTML con un lenguaje propio formado por
variables (`{{ ... }}`), filtros (`{{ variable|filtro }}`) y etiquetas
(`{% ... %}`). La lógica de presentación vive en la plantilla, mientras que la
vista se limita a preparar el contexto.

En este ejercicio debes completar la plantilla 'ej3d1/ficha.html' (en la carpeta
3d/templates/ej3d1/) para que muestre la ficha de un empleado, y la función
`renderizar_ficha()` que la renderiza con el contexto recibido.

La plantilla debe generar:

1. Un `<h1>` con el nombre del empleado capitalizado (filtro `title`).
2. Un `<p class="puesto">` con el puesto en mayúsculas (filtro `upper`).
3. Un `<p class="salario">` con el salario con dos decimales (filtro `floatformat`)
   seguido del símbolo `€`.
4. Un `<p class="alta">` con la fecha de alta en formato "d/m/Y" (filtro `date`).
5. Un `<p class="telefono">` con el teléfono o el texto "No disponible" si está
   vacío (filtro `default`).
6. Un `<p class="estado">` con el texto "Activo" o "Inactivo" según el valor de
   `empleado.activo` (etiqueta `{% if %}`).

La función `renderizar_ficha(empleado)` debe devolver el HTML resultante de
renderizar la plantilla con el contexto {"empleado": empleado}.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3d1_test.py).
"""

import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.template.loader import render_to_string  # noqa: E402


def renderizar_ficha(empleado):
    """
    Renderiza la plantilla 'ej3d1/ficha.html' con el empleado indicado y devuelve
    el HTML generado.
    """
    # TODO: Renderiza la plantilla y devuelve el HTML
    pass


if __name__ == "__main__":
    empleado = {
        "nombre": "ana lópez",
        "puesto": "desarrolladora web",
        "salario": 32450.5,
        "fecha_alta": date(2021, 3, 8),
        "telefono": "",
        "activo": True,
    }
    print(renderizar_ficha(empleado))
