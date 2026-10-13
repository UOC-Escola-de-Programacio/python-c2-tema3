"""
Tests del ejercicio ej3a2.py: API REST CRUD con Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import json

import pytest
from django.test import Client, override_settings

from ej3a2 import reiniciar_tareas


@pytest.fixture
def client():
    """Cliente de pruebas con el almacén de tareas vacío"""
    reiniciar_tareas()
    with override_settings(ROOT_URLCONF="ej3a2"):
        yield Client()


def crear_tarea(client, titulo, hecha=False):
    """Función auxiliar que crea una tarea a través de la API"""
    return client.post(
        "/api/tareas/",
        data=json.dumps({"titulo": titulo, "hecha": hecha}),
        content_type="application/json",
    )


def test_lista_vacia(client):
    """Sin tareas creadas, la colección está vacía"""
    respuesta = client.get("/api/tareas/")

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    assert json.loads(respuesta.content) == {"tareas": []}


def test_crear_tarea(client):
    """Una tarea creada con POST devuelve código 201 y la tarea creada"""
    respuesta = crear_tarea(client, "Estudiar Django")

    assert respuesta.status_code == 201, "Al crear un recurso se devuelve el código 201."
    tarea = json.loads(respuesta.content)
    assert tarea["id"] == 1, "La primera tarea creada debe tener el identificador 1."
    assert tarea["titulo"] == "Estudiar Django"
    assert tarea["hecha"] is False


def test_hecha_es_opcional(client):
    """El campo 'hecha' es opcional y por defecto vale False"""
    respuesta = client.post(
        "/api/tareas/",
        data=json.dumps({"titulo": "Leer la teoría"}),
        content_type="application/json",
    )

    assert respuesta.status_code == 201
    assert json.loads(respuesta.content)["hecha"] is False


def test_crear_tarea_sin_titulo(client):
    """Sin el campo 'titulo' la petición es inválida"""
    respuesta = client.post(
        "/api/tareas/", data=json.dumps({"hecha": True}), content_type="application/json"
    )

    assert respuesta.status_code == 400, "Sin título el código de estado debe ser 400."
    assert json.loads(respuesta.content) == {"error": "Datos inválidos"}


def test_crear_tarea_con_json_invalido(client):
    """Un cuerpo que no es JSON válido devuelve código 400"""
    respuesta = client.post(
        "/api/tareas/", data="esto no es json", content_type="application/json"
    )

    assert respuesta.status_code == 400, "Un JSON inválido debe devolver el código 400."


def test_listar_tareas_creadas(client):
    """Las tareas creadas aparecen en la colección"""
    crear_tarea(client, "Primera tarea")
    crear_tarea(client, "Segunda tarea", hecha=True)

    respuesta = client.get("/api/tareas/")
    tareas = json.loads(respuesta.content)["tareas"]

    assert len(tareas) == 2, "Deben devolverse las dos tareas creadas."
    assert [tarea["titulo"] for tarea in tareas] == ["Primera tarea", "Segunda tarea"]
    assert tareas[1]["hecha"] is True


def test_actualizar_tarea(client):
    """PUT actualiza los campos indicados de la tarea"""
    crear_tarea(client, "Tarea inicial")

    respuesta = client.put(
        "/api/tareas/1/",
        data=json.dumps({"titulo": "Tarea actualizada", "hecha": True}),
        content_type="application/json",
    )

    assert respuesta.status_code == 200, "El código de estado debe ser 200."
    tarea = json.loads(respuesta.content)
    assert tarea["titulo"] == "Tarea actualizada"
    assert tarea["hecha"] is True


def test_actualizar_tarea_parcialmente(client):
    """Los campos que no se envían mantienen su valor"""
    crear_tarea(client, "Tarea inicial")

    respuesta = client.put(
        "/api/tareas/1/", data=json.dumps({"hecha": True}), content_type="application/json"
    )

    tarea = json.loads(respuesta.content)
    assert tarea["titulo"] == "Tarea inicial", "El título no enviado no debe modificarse."
    assert tarea["hecha"] is True


def test_actualizar_tarea_inexistente(client):
    """Actualizar una tarea que no existe devuelve código 404"""
    respuesta = client.put(
        "/api/tareas/42/",
        data=json.dumps({"titulo": "No existe"}),
        content_type="application/json",
    )

    assert respuesta.status_code == 404, "El código de estado debe ser 404."
    assert json.loads(respuesta.content) == {"error": "Tarea no encontrada"}


def test_eliminar_tarea(client):
    """DELETE elimina la tarea y devuelve código 204 sin contenido"""
    crear_tarea(client, "Tarea a borrar")

    respuesta = client.delete("/api/tareas/1/")

    assert respuesta.status_code == 204, "Al eliminar un recurso se devuelve el código 204."
    assert respuesta.content == b"", "La respuesta 204 no debe tener contenido."
    assert json.loads(client.get("/api/tareas/").content)["tareas"] == []


def test_eliminar_tarea_inexistente(client):
    """Eliminar una tarea que no existe devuelve código 404"""
    respuesta = client.delete("/api/tareas/7/")

    assert respuesta.status_code == 404, "El código de estado debe ser 404."


def test_metodo_no_permitido(client):
    """Los métodos no soportados devuelven código 405"""
    crear_tarea(client, "Tarea")

    assert client.delete("/api/tareas/").status_code == 405, (
        "DELETE sobre la colección no está permitido."
    )
    assert client.post("/api/tareas/1/").status_code == 405, (
        "POST sobre una tarea concreta no está permitido."
    )
