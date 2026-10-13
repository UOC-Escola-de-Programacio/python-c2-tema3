"""
Configuración común de pytest para los ejercicios del tema.

Prepara Django antes de que se importen los ficheros de los ejercicios.
No es necesario que modifiques este fichero.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ejercicios.config import configurar_django  # noqa: E402

configurar_django()

from django.test.utils import setup_test_environment  # noqa: E402

# Permite que las respuestas del cliente de pruebas incluyan las plantillas
# utilizadas y su contexto.
setup_test_environment()
