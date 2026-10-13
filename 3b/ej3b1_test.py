"""
Tests del ejercicio ej3b1.py: patrón MVT (Modelo-Vista-Plantilla) con Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import pytest
from django.http import Http404
from django.test import Client, RequestFactory, override_settings

from ej3b1 import buscar_curso, detalle_curso, obtener_cursos


@pytest.fixture
def client():
    """Cliente de pruebas de Django que utiliza las rutas definidas en ej3b1.py"""
    with override_settings(ROOT_URLCONF="ej3b1"):
        yield Client()


def test_obtener_cursos():
    """El modelo devuelve todos los cursos"""
    cursos = obtener_cursos()

    assert len(cursos) == 3, "El catálogo tiene 3 cursos."
    assert {curso["slug"] for curso in cursos} == {"python-basico", "django", "apis-rest"}


def test_buscar_curso():
    """El modelo permite buscar un curso por su slug"""
    curso = buscar_curso("django")

    assert curso is not None, "El curso 'django' existe en el catálogo."
    assert curso["nombre"] == "Desarrollo web con Django"


def test_buscar_curso_inexistente():
    """Si el curso no existe, el modelo devuelve None"""
    assert buscar_curso("no-existe") is None


def test_lista_cursos_usa_la_plantilla(client):
    """La vista de listado renderiza la plantilla con todos los cursos"""
    respuesta = client.get("/cursos/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    html = respuesta.content.decode("utf-8")
    assert "Desarrollo web con Django" in html, "La plantilla debe mostrar los cursos."
    assert "Diseño de APIs REST" in html
    assert "/cursos/django/" in html, "El listado debe enlazar con el detalle de cada curso."


def test_detalle_curso(client):
    """La vista de detalle muestra la información de un curso"""
    respuesta = client.get("/cursos/apis-rest/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    html = respuesta.content.decode("utf-8")
    assert "Diseño de APIs REST" in html
    assert "Avanzado" in html, "El detalle debe mostrar el nivel del curso."
    assert "20" in html, "El detalle debe mostrar la duración del curso."


def test_detalle_curso_inexistente_devuelve_404(client):
    """Un curso inexistente produce una respuesta 404"""
    respuesta = client.get("/cursos/no-existe/")

    assert respuesta.status_code == 404, "El código de estado debe ser 404."


def test_detalle_curso_lanza_http404():
    """La vista lanza Http404 cuando el curso no existe"""
    peticion = RequestFactory().get("/cursos/no-existe/")

    with pytest.raises(Http404):
        detalle_curso(peticion, "no-existe")


def test_las_vistas_no_generan_el_html(client):
    """La presentación es responsabilidad de la plantilla, no de la vista"""
    respuesta = client.get("/cursos/")

    plantillas = [plantilla.name for plantilla in respuesta.templates]
    assert "ej3b1/lista_cursos.html" in plantillas, (
        "La vista debe usar render() con la plantilla 'ej3b1/lista_cursos.html'."
    )
    assert "cursos" in respuesta.context, (
        "La vista debe pasar los cursos a la plantilla en el contexto."
    )
