"""
Enunciado:
Django organiza las aplicaciones siguiendo el patrón MVT (Modelo-Vista-Plantilla),
la variante del patrón MVC que utiliza este framework:

- El **modelo** contiene los datos y la lógica de negocio.
- La **vista** recibe la petición, pide los datos al modelo y elige la plantilla.
- La **plantilla** (la "vista" del MVC clásico) se encarga de la presentación.
- El fichero de **rutas** (urls) actúa de controlador frontal y decide qué vista
  atiende cada URL.

En este ejercicio separarás correctamente esas responsabilidades para un catálogo
de cursos. Debes implementar:

1. `obtener_cursos()`: función del modelo que devuelve la lista completa de cursos.
2. `buscar_curso(slug)`: función del modelo que devuelve el curso con ese `slug` o
   `None` si no existe.
3. `lista_cursos(request)`: vista que renderiza la plantilla
   'ej3b1/lista_cursos.html' con el contexto {"cursos": [...]}.
4. `detalle_curso(request, slug)`: vista que renderiza la plantilla
   'ej3b1/detalle_curso.html' con el contexto {"curso": {...}}. Si el curso no
   existe debe lanzar `Http404`.
5. Las rutas `/cursos/` y `/cursos/<slug>/` en `urlpatterns`, con los nombres
   'lista-cursos' y 'detalle-curso'.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3b1_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.http import Http404  # noqa: E402
from django.shortcuts import render  # noqa: E402
from django.urls import path  # noqa: E402

# --- Modelo -----------------------------------------------------------------
# En este ejercicio los datos están en memoria; en el siguiente apartado usarás
# el ORM de Django para guardarlos en una base de datos.
CURSOS = [
    {"slug": "python-basico", "nombre": "Python básico", "horas": 30, "nivel": "Inicial"},
    {"slug": "django", "nombre": "Desarrollo web con Django", "horas": 45, "nivel": "Medio"},
    {"slug": "apis-rest", "nombre": "Diseño de APIs REST", "horas": 20, "nivel": "Avanzado"},
]


def obtener_cursos():
    """
    Devuelve la lista de todos los cursos.
    """
    # TODO: Implementa la función
    pass


def buscar_curso(slug):
    """
    Devuelve el curso cuyo `slug` coincide con el indicado, o None si no existe.
    """
    # TODO: Implementa la función
    pass


# --- Vistas -----------------------------------------------------------------
def lista_cursos(request):
    """
    Muestra el listado de cursos usando la plantilla 'ej3b1/lista_cursos.html'.
    """
    # TODO: Implementa la vista
    pass


def detalle_curso(request, slug):
    """
    Muestra un curso concreto usando la plantilla 'ej3b1/detalle_curso.html'.
    Si el curso no existe, lanza Http404.
    """
    # TODO: Implementa la vista
    pass


# --- Rutas (controlador frontal) --------------------------------------------
# TODO: Define las rutas del catálogo usando path()
urlpatterns = []

if __name__ == "__main__":
    from django.conf import settings
    from django.core.management import execute_from_command_line

    settings.ROOT_URLCONF = __name__
    execute_from_command_line([sys.argv[0], "runserver", "--noreload"])
