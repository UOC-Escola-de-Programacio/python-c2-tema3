"""
Tests del ejercicio ej3b2.py: vistas basadas en clases y patrón POST/Redirect/GET.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import pytest
from django.test import Client, override_settings
from django.views import View

from ej3b2 import INSCRIPCIONES, InscripcionView, reiniciar_inscripciones


@pytest.fixture
def client():
    """Cliente de pruebas sin inscripciones previas"""
    reiniciar_inscripciones()
    with override_settings(ROOT_URLCONF="ej3b2"):
        yield Client()


def test_es_una_vista_basada_en_clase():
    """La inscripción debe implementarse con una vista basada en clase"""
    assert issubclass(InscripcionView, View), "InscripcionView debe heredar de django.views.View."


def test_get_muestra_el_formulario(client):
    """GET muestra el formulario de inscripción"""
    respuesta = client.get("/inscripcion/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    plantillas = [plantilla.name for plantilla in respuesta.templates]
    assert "ej3b2/inscripcion.html" in plantillas, (
        "Debe renderizarse la plantilla 'ej3b2/inscripcion.html'."
    )
    assert respuesta.context["errores"] == [], "El formulario inicial no tiene errores."


def test_post_valido_redirige(client):
    """Un formulario correcto guarda la inscripción y redirige"""
    respuesta = client.post(
        "/inscripcion/", {"nombre": "Ana", "email": "ana@example.com"}
    )

    assert respuesta.status_code == 302, "Tras un POST correcto debe redirigirse (código 302)."
    assert respuesta["Location"] == "/gracias/", "La redirección debe apuntar a /gracias/."
    assert INSCRIPCIONES == [{"nombre": "Ana", "email": "ana@example.com"}]


def test_post_sin_nombre(client):
    """Sin nombre se vuelve a mostrar el formulario con el error"""
    respuesta = client.post("/inscripcion/", {"nombre": "", "email": "ana@example.com"})

    assert respuesta.status_code == 200, "Con errores se vuelve a mostrar el formulario."
    assert "El nombre es obligatorio" in respuesta.context["errores"]
    assert INSCRIPCIONES == [], "No debe guardarse una inscripción inválida."


def test_post_con_email_invalido(client):
    """Un email sin '@' produce un error de validación"""
    respuesta = client.post("/inscripcion/", {"nombre": "Ana", "email": "ana.example.com"})

    assert respuesta.status_code == 200
    assert "El email no es válido" in respuesta.context["errores"]
    assert INSCRIPCIONES == []


def test_post_mantiene_los_datos_introducidos(client):
    """Al mostrar los errores se conservan los datos que escribió el usuario"""
    respuesta = client.post("/inscripcion/", {"nombre": "Ana", "email": "ana.example.com"})

    assert respuesta.context["nombre"] == "Ana", (
        "El nombre introducido debe conservarse en el contexto."
    )
    assert respuesta.context["email"] == "ana.example.com"
    assert "Ana" in respuesta.content.decode("utf-8")


def test_pagina_de_gracias(client):
    """La página de gracias muestra el total de inscripciones"""
    client.post("/inscripcion/", {"nombre": "Ana", "email": "ana@example.com"})
    client.post("/inscripcion/", {"nombre": "Luis", "email": "luis@example.com"})

    respuesta = client.get("/gracias/")

    assert respuesta.status_code == 200
    assert respuesta.context["total"] == 2, "Deben contarse las dos inscripciones."
    assert "2" in respuesta.content.decode("utf-8")


def test_flujo_completo(client):
    """Se puede seguir la redirección hasta la página de confirmación"""
    respuesta = client.post(
        "/inscripcion/", {"nombre": "Ana", "email": "ana@example.com"}, follow=True
    )

    assert respuesta.status_code == 200
    plantillas = [plantilla.name for plantilla in respuesta.templates]
    assert "ej3b2/gracias.html" in plantillas, (
        "Tras la redirección debe mostrarse la plantilla 'ej3b2/gracias.html'."
    )
