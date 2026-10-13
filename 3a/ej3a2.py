"""
Enunciado:
Una API REST completa no solo permite consultar recursos, también crearlos,
modificarlos y eliminarlos. En este ejercicio implementarás una API CRUD sobre una
colección de tareas guardada en memoria, prestando atención a los códigos de estado
HTTP y al cuerpo JSON de las peticiones.

Debes implementar los siguientes endpoints:

1. `GET /api/tareas/`: devuelve {"tareas": [...]} con código 200.
2. `POST /api/tareas/`: crea una tarea a partir del JSON recibido
   ({"titulo": "...", "hecha": false}). Devuelve la tarea creada (con su `id`) y
   código 201. Si falta el campo `titulo` o el cuerpo no es JSON válido, devuelve
   {"error": "Datos inválidos"} con código 400. El campo `hecha` es opcional y su
   valor por defecto es False.
3. `PUT /api/tareas/<id>/`: actualiza los campos `titulo` y/o `hecha` de la tarea y
   devuelve la tarea actualizada con código 200.
4. `DELETE /api/tareas/<id>/`: elimina la tarea y devuelve una respuesta vacía con
   código 204.
5. En `PUT` y `DELETE`, si la tarea no existe devuelve {"error": "Tarea no encontrada"}
   con código 404.
6. Cualquier otro método sobre esos endpoints debe devolver el código 405.

Tu tarea es completar las vistas `coleccion_tareas` y `recurso_tarea` y las rutas.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3a2_test.py).
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.http import HttpResponse, JsonResponse  # noqa: E402
from django.urls import path  # noqa: E402
from django.views.decorators.csrf import csrf_exempt  # noqa: E402

# Almacén de tareas en memoria. La clave es el identificador de la tarea.
TAREAS = {}
# Último identificador asignado.
ULTIMO_ID = 0


def reiniciar_tareas():
    """
    Vacía el almacén de tareas. Se utiliza en los tests para partir de un estado
    conocido. No es necesario modificar esta función.
    """
    global ULTIMO_ID
    TAREAS.clear()
    ULTIMO_ID = 0


def _leer_json(request):
    """
    Devuelve el cuerpo JSON de la petición o None si no es un JSON válido.
    """
    try:
        return json.loads(request.body)
    except (ValueError, TypeError):
        return None


@csrf_exempt
def coleccion_tareas(request):
    """
    Gestiona la colección de tareas:
    - GET: devuelve {"tareas": [...]} con código 200.
    - POST: crea una tarea nueva y la devuelve con código 201.
    """
    global ULTIMO_ID

    # TODO: Implementa la vista
    pass


@csrf_exempt
def recurso_tarea(request, tarea_id):
    """
    Gestiona una tarea concreta:
    - PUT: actualiza la tarea y la devuelve con código 200.
    - DELETE: elimina la tarea y devuelve una respuesta vacía con código 204.
    """
    # TODO: Implementa la vista
    pass


# Rutas de la API: /api/tareas/ y /api/tareas/<id>/
# TODO: Define las rutas de la API usando path()
urlpatterns = []

if __name__ == "__main__":
    from django.conf import settings
    from django.core.management import execute_from_command_line

    settings.ROOT_URLCONF = __name__
    execute_from_command_line([sys.argv[0], "runserver", "--noreload"])
