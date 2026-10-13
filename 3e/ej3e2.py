"""
Enunciado:
La herencia de plantillas de Django puede tener varios niveles: una plantilla base
general, plantillas intermedias para cada sección del sitio y plantillas concretas
para cada página. Además, con `{% include %}` se pueden reutilizar fragmentos de
HTML pasándoles su propio contexto mediante `with`.

En este ejercicio construirás una jerarquía de tres niveles para el blog de un
sitio web, en la carpeta 3e/templates/ej3e2/:

1. 'base.html' (nivel 1), con:
   - `<title>` con el bloque `titulo` (por defecto "Mi sitio").
   - `<nav class="menu">Inicio</nav>`.
   - el bloque `contenido`.
   - el bloque `lateral`, vacío por defecto.
2. 'base_blog.html' (nivel 2), que extiende 'base.html' y:
   - define el bloque `lateral` con `<aside class="lateral">Últimas entradas</aside>`.
   - define el bloque `contenido` con `<article class="entrada">` que contiene, a
     su vez, un bloque llamado `cuerpo`.
3. 'articulo.html' (nivel 3), que extiende 'base_blog.html' y define:
   - el bloque `titulo` con el título de la entrada.
   - el bloque `cuerpo` con `<h2 class="titular">{{ entrada.titulo }}</h2>`,
     `<p class="texto">{{ entrada.texto }}</p>` y la inclusión del fragmento
     '_etiquetas.html' pasándole las etiquetas de la entrada con
     `{% include ... with etiquetas=entrada.etiquetas %}`.
4. '_etiquetas.html', el fragmento reutilizable, con un `<ul class="etiquetas">`
   que contiene un `<li>` por etiqueta.

La función `renderizar_articulo()` renderiza la plantilla de la entrada.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3e2_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.template.loader import render_to_string  # noqa: E402


def renderizar_articulo(entrada):
    """
    Renderiza la plantilla 'ej3e2/articulo.html' con la entrada indicada.
    """
    # TODO: Renderiza la plantilla y devuelve el HTML
    pass


if __name__ == "__main__":
    entrada = {
        "titulo": "Primeros pasos con Django",
        "texto": "Django es un framework web escrito en Python.",
        "etiquetas": ["python", "django", "web"],
    }
    print(renderizar_articulo(entrada))
