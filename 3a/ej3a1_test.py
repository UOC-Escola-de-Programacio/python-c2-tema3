"""
Tests del ejercicio ej3a1.py: API REST de solo lectura con Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import json

import pytest
from django.test import Client, override_settings

from ej3a1 import detalle_libro, lista_libros, urlpatterns


@pytest.fixture
def client():
    """Cliente de pruebas de Django que utiliza las rutas definidas en ej3a1.py"""
    with override_settings(ROOT_URLCONF="ej3a1"):
        yield Client()


def test_rutas_definidas():
    """Comprueba que se han definido las dos rutas de la API"""
    vistas = {ruta.callback for ruta in urlpatterns}
    assert lista_libros in vistas, "Debe existir una ruta asociada a la vista lista_libros."
    assert detalle_libro in vistas, "Debe existir una ruta asociada a la vista detalle_libro."


def test_lista_libros(client):
    """La lista de libros se devuelve en JSON con código 200"""
    respuesta = client.get("/api/libros/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    assert respuesta["Content-Type"].startswith("application/json"), (
        "La respuesta debe ser de tipo application/json."
    )

    datos = json.loads(respuesta.content)
    assert "libros" in datos, "La respuesta debe tener la forma {'libros': [...]}."
    assert len(datos["libros"]) == 4, "Deben devolverse los 4 libros del catálogo."
    assert datos["libros"][0]["titulo"] == "Cien años de soledad"


def test_lista_libros_filtrada_por_genero(client):
    """El parámetro de consulta 'genero' filtra los resultados"""
    respuesta = client.get("/api/libros/", {"genero": "Cuento"})

    assert respuesta.status_code == 200
    datos = json.loads(respuesta.content)
    assert len(datos["libros"]) == 1, "Solo un libro pertenece al género 'Cuento'."
    assert datos["libros"][0]["titulo"] == "Ficciones"


def test_lista_libros_filtro_sin_distinguir_mayusculas(client):
    """El filtro por género no distingue mayúsculas de minúsculas"""
    respuesta = client.get("/api/libros/", {"genero": "novela"})

    assert respuesta.status_code == 200
    datos = json.loads(respuesta.content)
    assert len(datos["libros"]) == 1, "El filtro debe ignorar mayúsculas y minúsculas."
    assert datos["libros"][0]["titulo"] == "Rayuela"


def test_lista_libros_genero_inexistente(client):
    """Si ningún libro coincide con el género se devuelve una lista vacía"""
    respuesta = client.get("/api/libros/", {"genero": "Poesía"})

    assert respuesta.status_code == 200
    assert json.loads(respuesta.content)["libros"] == []


def test_detalle_libro(client):
    """El detalle de un libro existente se devuelve con código 200"""
    respuesta = client.get("/api/libros/3/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    datos = json.loads(respuesta.content)
    assert datos["id"] == 3
    assert datos["titulo"] == "Ficciones"
    assert datos["anio"] == 1944


def test_detalle_libro_inexistente(client):
    """Si el libro no existe se devuelve un error 404"""
    respuesta = client.get("/api/libros/99/")

    assert respuesta.status_code == 404, "El código de estado debe ser 404."
    assert json.loads(respuesta.content) == {"error": "Libro no encontrado"}
