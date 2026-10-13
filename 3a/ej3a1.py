"""
Enunciado:
Django permite construir APIs REST utilizando vistas que devuelven documentos JSON
en lugar de páginas HTML. En este ejercicio crearás una pequeña API de solo lectura
sobre un catálogo de libros guardado en memoria.

Debes implementar los siguientes endpoints:

1. `GET /api/libros/`: devuelve un JSON con la forma {"libros": [...]} y código 200.
   Si se recibe el parámetro de consulta `genero`, solo deben devolverse los libros
   de ese género (la comparación no distingue mayúsculas de minúsculas).
2. `GET /api/libros/<id>/`: devuelve el libro con ese identificador y código 200.
   Si el libro no existe, devuelve {"error": "Libro no encontrado"} con código 404.

Además debes definir la lista `urlpatterns` que asocia cada ruta con su vista.

Tu tarea es completar las vistas `lista_libros` y `detalle_libro` y las rutas.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3a1_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.http import JsonResponse  # noqa: E402
from django.urls import path  # noqa: E402

# Catálogo de libros utilizado como origen de datos de la API.
LIBROS = [
    {"id": 1, "titulo": "Cien años de soledad", "genero": "Realismo mágico", "anio": 1967},
    {"id": 2, "titulo": "La casa de los espíritus", "genero": "Realismo mágico", "anio": 1982},
    {"id": 3, "titulo": "Ficciones", "genero": "Cuento", "anio": 1944},
    {"id": 4, "titulo": "Rayuela", "genero": "Novela", "anio": 1963},
]


def lista_libros(request):
    """
    Devuelve la lista de libros en formato JSON: {"libros": [...]}.
    Si la petición incluye el parámetro `genero`, filtra los libros por ese género.
    """
    # TODO: Implementa la vista
    pass


def detalle_libro(request, libro_id):
    """
    Devuelve el libro cuyo identificador es `libro_id`.
    Si no existe, devuelve {"error": "Libro no encontrado"} con código 404.
    """
    # TODO: Implementa la vista
    pass


# Rutas de la API: /api/libros/ y /api/libros/<id>/
# TODO: Define las rutas de la API usando path()
urlpatterns = []

if __name__ == "__main__":
    from django.conf import settings
    from django.core.management import execute_from_command_line

    # Levanta el servidor de desarrollo usando las rutas de este fichero.
    settings.ROOT_URLCONF = __name__
    execute_from_command_line([sys.argv[0], "runserver", "--noreload"])
