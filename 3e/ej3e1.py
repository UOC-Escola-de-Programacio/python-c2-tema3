"""
Enunciado:
La herencia de plantillas evita repetir el HTML común de un sitio web. Una
plantilla base define la estructura y una serie de bloques (`{% block %}`), y las
plantillas hijas la extienden (`{% extends %}`) rellenando o sustituyendo esos
bloques. Con `{{ block.super }}` una plantilla hija puede reutilizar el contenido
del bloque del padre y añadirle algo.

En este ejercicio debes completar tres plantillas de la carpeta 3e/templates/ej3e1/:

1. 'base.html', con:
   - `<title>` cuyo contenido es el bloque `titulo`, con el valor por defecto
     "Escuela de Programación".
   - `<h1 class="marca">Escuela de Programación</h1>`.
   - `<main>` con el bloque `contenido` (vacío por defecto).
   - `<footer class="pie">` con el bloque `pie`, cuyo contenido por defecto es
     "Todos los derechos reservados".
2. 'inicio.html', que extiende 'base.html' y define:
   - el bloque `titulo` con el texto "Inicio".
   - el bloque `contenido` con `<p class="mensaje">Hola, {{ nombre }}</p>`.
3. 'contacto.html', que extiende 'base.html' y define:
   - el bloque `titulo` con el texto "Contacto".
   - el bloque `contenido` con `<p class="email">{{ email }}</p>`.
   - el bloque `pie`, que debe conservar el contenido del padre con
     `{{ block.super }}` y añadir a continuación " | Escríbenos".

Las funciones `renderizar_inicio()` y `renderizar_contacto()` renderizan las
plantillas hijas con su contexto.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3e1_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.template.loader import render_to_string  # noqa: E402


def renderizar_inicio(nombre):
    """
    Renderiza la plantilla 'ej3e1/inicio.html' con el nombre indicado.
    """
    # TODO: Renderiza la plantilla y devuelve el HTML
    pass


def renderizar_contacto(email):
    """
    Renderiza la plantilla 'ej3e1/contacto.html' con el email indicado.
    """
    # TODO: Renderiza la plantilla y devuelve el HTML
    pass


if __name__ == "__main__":
    print(renderizar_inicio("Ana"))
    print(renderizar_contacto("info@example.com"))
