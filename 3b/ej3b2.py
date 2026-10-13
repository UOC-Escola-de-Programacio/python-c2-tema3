"""
Enunciado:
Además de las vistas basadas en funciones, Django ofrece vistas basadas en clases
(Class-Based Views). Al heredar de `django.views.View`, cada método HTTP se atiende
con un método de la clase: `get()` para GET, `post()` para POST, etc.

En este ejercicio implementarás el flujo clásico de un formulario web, donde la
vista actúa como controlador: muestra el formulario, valida los datos recibidos y,
si son correctos, redirige a otra página (patrón POST/Redirect/GET).

Debes implementar:

1. `InscripcionView(View)`:
   - `get()`: renderiza la plantilla 'ej3b2/inscripcion.html' con el contexto
     {"errores": []}.
   - `post()`: lee los campos `nombre` y `email` de `request.POST`.
     * Si falta el nombre, añade el error "El nombre es obligatorio".
     * Si el email no contiene el carácter "@", añade el error "El email no es válido".
     * Si hay errores, vuelve a renderizar la plantilla con el contexto
       {"errores": [...], "nombre": nombre, "email": email} y código 200.
     * Si no hay errores, guarda la inscripción con `guardar_inscripcion(nombre, email)`
       y redirige (código 302) a la URL con nombre 'gracias' usando `redirect()`.
2. `gracias(request)`: vista basada en función que renderiza la plantilla
   'ej3b2/gracias.html' con el contexto {"total": <número de inscripciones>}.
3. Las rutas `/inscripcion/` (nombre 'inscripcion') y `/gracias/` (nombre 'gracias').

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3b2_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.shortcuts import redirect, render  # noqa: E402
from django.urls import path  # noqa: E402
from django.views import View  # noqa: E402

# Inscripciones guardadas (modelo en memoria).
INSCRIPCIONES = []


def guardar_inscripcion(nombre, email):
    """
    Guarda una inscripción. No es necesario modificar esta función.
    """
    INSCRIPCIONES.append({"nombre": nombre, "email": email})


def reiniciar_inscripciones():
    """
    Elimina todas las inscripciones. Se utiliza en los tests.
    """
    INSCRIPCIONES.clear()


class InscripcionView(View):
    """
    Vista basada en clase que muestra y procesa el formulario de inscripción.
    """

    def get(self, request):
        """Muestra el formulario vacío."""
        # TODO: Implementa el método
        pass

    def post(self, request):
        """Valida el formulario y, si es correcto, redirige a la página de gracias."""
        # TODO: Implementa el método
        pass


def gracias(request):
    """
    Muestra la confirmación de la inscripción y el total de inscritos.
    """
    # TODO: Implementa la vista
    pass


# TODO: Define las rutas del formulario usando path()
urlpatterns = []

if __name__ == "__main__":
    from django.conf import settings
    from django.core.management import execute_from_command_line

    settings.ROOT_URLCONF = __name__
    execute_from_command_line([sys.argv[0], "runserver", "--noreload"])
