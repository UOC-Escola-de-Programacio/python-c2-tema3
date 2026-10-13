"""
Tests del ejercicio ej3c1.py: modelos y operaciones CRUD con el ORM de Django.

Si deseas cambiar el idioma del ejercicio, edita este archivo.
"""

import pytest
from django.db import models

from ejercicios.config import tablas

from ej3c1 import (
    Autor,
    Libro,
    actualizar_anio,
    crear_autor,
    crear_libro,
    eliminar_libro,
    libros_de_autor,
)


@pytest.fixture
def bd():
    """Crea las tablas de los modelos para cada test y las elimina al terminar"""
    with tablas(Autor, Libro):
        yield


@pytest.fixture
def datos(bd):
    """Inserta un conjunto de datos de ejemplo"""
    garcia = crear_autor("Gabriel García Márquez", "Colombiana")
    allende = crear_autor("Isabel Allende", "Chilena")
    crear_libro("Cien años de soledad", 1967, garcia)
    crear_libro("El amor en los tiempos del cólera", 1985, garcia)
    crear_libro("La casa de los espíritus", 1982, allende)
    return {"garcia": garcia, "allende": allende}


def test_campos_del_modelo_autor():
    """El modelo Autor define los campos pedidos"""
    nombre = Autor._meta.get_field("nombre")
    nacionalidad = Autor._meta.get_field("nacionalidad")

    assert isinstance(nombre, models.CharField), "'nombre' debe ser un CharField."
    assert nombre.max_length == 100, "'nombre' debe admitir hasta 100 caracteres."
    assert isinstance(nacionalidad, models.CharField), "'nacionalidad' debe ser un CharField."
    assert nacionalidad.max_length == 50
    assert nacionalidad.blank is True, "'nacionalidad' debe ser opcional (blank=True)."


def test_ordenacion_del_modelo_autor():
    """Los autores se ordenan por nombre"""
    assert list(Autor._meta.ordering) == ["nombre"], (
        "Autor.Meta.ordering debe ordenar por 'nombre'."
    )


def test_campos_del_modelo_libro():
    """El modelo Libro define los campos pedidos y la relación con Autor"""
    titulo = Libro._meta.get_field("titulo")
    anio = Libro._meta.get_field("anio")
    autor = Libro._meta.get_field("autor")

    assert isinstance(titulo, models.CharField) and titulo.max_length == 200
    assert isinstance(anio, models.IntegerField), "'anio' debe ser un IntegerField."
    assert isinstance(autor, models.ForeignKey), "'autor' debe ser una ForeignKey a Autor."
    assert autor.related_model is Autor
    assert autor.remote_field.related_name == "libros", (
        "La relación inversa debe llamarse 'libros'."
    )
    assert autor.remote_field.on_delete is models.CASCADE, (
        "Al borrar un autor deben borrarse sus libros (on_delete=models.CASCADE)."
    )


def test_str_de_los_modelos(bd):
    """El método __str__ devuelve una representación legible"""
    autor = crear_autor("Jorge Luis Borges", "Argentina")
    libro = crear_libro("Ficciones", 1944, autor)

    assert str(autor) == "Jorge Luis Borges"
    assert str(libro) == "Ficciones (1944)"


def test_crear_autor(bd):
    """crear_autor guarda el autor en la base de datos"""
    autor = crear_autor("Isabel Allende", "Chilena")

    assert autor.pk is not None, "El autor debe estar guardado en la base de datos."
    assert Autor.objects.count() == 1
    assert Autor.objects.first().nacionalidad == "Chilena"


def test_crear_libro(bd):
    """crear_libro asocia el libro con su autor"""
    autor = crear_autor("Isabel Allende")
    libro = crear_libro("Paula", 1994, autor)

    assert libro.pk is not None
    assert libro.autor == autor
    assert list(autor.libros.all()) == [libro], (
        "Debe poder accederse a los libros con autor.libros.all()."
    )


def test_libros_de_autor(datos):
    """libros_de_autor filtra los libros por el nombre del autor"""
    libros = libros_de_autor("Gabriel García Márquez")

    assert libros.count() == 2, "García Márquez tiene dos libros en los datos de ejemplo."
    titulos = [libro.titulo for libro in libros]
    assert "Cien años de soledad" in titulos
    assert "La casa de los espíritus" not in titulos


def test_libros_de_autor_inexistente(datos):
    """Si el autor no existe el resultado está vacío"""
    assert libros_de_autor("Autor Inexistente").count() == 0


def test_actualizar_anio(datos):
    """actualizar_anio modifica el libro en la base de datos"""
    libro = actualizar_anio("Cien años de soledad", 1968)

    assert libro is not None
    assert libro.anio == 1968
    assert Libro.objects.get(titulo="Cien años de soledad").anio == 1968, (
        "El cambio debe guardarse en la base de datos con save()."
    )


def test_actualizar_anio_libro_inexistente(datos):
    """Si el libro no existe se devuelve None"""
    assert actualizar_anio("No existe", 2000) is None


def test_eliminar_libro(datos):
    """eliminar_libro borra el libro y devuelve cuántos se han eliminado"""
    eliminados = eliminar_libro("Cien años de soledad")

    assert eliminados == 1, "Debe eliminarse un único libro."
    assert Libro.objects.filter(titulo="Cien años de soledad").count() == 0
    assert Libro.objects.count() == 2


def test_eliminar_libro_inexistente(datos):
    """Si el libro no existe no se elimina nada"""
    assert eliminar_libro("No existe") == 0
    assert Libro.objects.count() == 3


def test_borrado_en_cascada(datos):
    """Al eliminar un autor se eliminan sus libros"""
    datos["garcia"].delete()

    assert Libro.objects.count() == 1, "Solo debe quedar el libro de Isabel Allende."
