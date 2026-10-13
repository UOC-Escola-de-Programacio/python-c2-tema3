"""
Configuración mínima de Django utilizada por todos los ejercicios del tema.

En un proyecto real esta configuración vive en el fichero 'settings.py' que genera
el comando 'django-admin startproject'. Aquí se define mediante
'settings.configure()' para que cada ejercicio pueda ser un único fichero Python.

No es necesario que modifiques este fichero.
"""

import sys
from contextlib import contextmanager
from pathlib import Path

import django
from django.conf import settings

# Carpeta raíz del repositorio (la que contiene las carpetas 3a, 3b, 3c...).
RAIZ = Path(__file__).resolve().parent.parent


def configurar_django():
    """
    Configura Django (una sola vez) para poder ejecutar los ejercicios y sus tests.
    """
    if str(RAIZ) not in sys.path:
        sys.path.insert(0, str(RAIZ))

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY="clave-de-pruebas-del-tema-3",
            ALLOWED_HOSTS=["*"],
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "django.contrib.messages",
                "django.contrib.sessions",
                "django.contrib.admin",
                "django.contrib.staticfiles",
                "ejercicios",
            ],
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            MIDDLEWARE=[
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ],
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    # Todas las carpetas 'templates' de los apartados del tema.
                    "DIRS": sorted(str(ruta) for ruta in RAIZ.glob("3*/templates")),
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ]
                    },
                }
            ],
            ROOT_URLCONF="ejercicios.urls",
            STATIC_URL="/static/",
            USE_TZ=True,
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        )
        django.setup()


@contextmanager
def tablas(*modelos):
    """
    Crea en la base de datos de pruebas las tablas de los modelos indicados y las
    elimina al terminar. Se utiliza en los tests de los ejercicios con modelos.
    """
    from django.db import connection

    with connection.schema_editor() as editor:
        for modelo in modelos:
            editor.create_model(modelo)
    try:
        yield
    finally:
        with connection.schema_editor() as editor:
            for modelo in reversed(modelos):
                editor.delete_model(modelo)
