"""
Enunciado:
El ORM (Object-Relational Mapping) de Django permite trabajar con la base de datos
usando clases de Python en lugar de escribir SQL. Cada modelo es una clase que
hereda de `django.db.models.Model` y cada atributo es una columna de la tabla.

En este ejercicio definirás los modelos de una pequeña biblioteca y las operaciones
básicas sobre ellos (crear, leer, actualizar y borrar).

Debes implementar:

1. El modelo `Autor` con los campos:
   - `nombre`: texto de hasta 100 caracteres.
   - `nacionalidad`: texto de hasta 50 caracteres, opcional (puede quedar vacío).
   Su método `__str__` debe devolver el nombre y los autores deben ordenarse por
   nombre de forma ascendente.
2. El modelo `Libro` con los campos:
   - `titulo`: texto de hasta 200 caracteres.
   - `anio`: número entero.
   - `autor`: clave foránea a `Autor`, con borrado en cascada y nombre inverso
     `libros` (para poder escribir `autor.libros.all()`).
   Su método `__str__` debe devolver "<titulo> (<anio>)".
3. Las funciones `crear_autor`, `crear_libro`, `libros_de_autor`,
   `actualizar_anio` y `eliminar_libro` descritas más abajo.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3c1_test.py).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.db import models  # noqa: E402


class Autor(models.Model):
    """
    Autor de uno o varios libros.
    """

    # TODO: Define los campos `nombre` y `nacionalidad`

    class Meta:
        # Los modelos de los ejercicios pertenecen a la aplicación 'ejercicios'.
        app_label = "ejercicios"
        # TODO: Ordena los autores por nombre de forma ascendente

    def __str__(self):
        # TODO: Devuelve el nombre del autor
        pass


class Libro(models.Model):
    """
    Libro escrito por un autor.
    """

    # TODO: Define los campos `titulo`, `anio` y `autor`

    class Meta:
        app_label = "ejercicios"
        ordering = ["anio"]

    def __str__(self):
        # TODO: Devuelve "<titulo> (<anio>)"
        pass


def crear_autor(nombre, nacionalidad=""):
    """
    Crea y devuelve un autor.
    """
    # TODO: Implementa la función
    pass


def crear_libro(titulo, anio, autor):
    """
    Crea y devuelve un libro asociado al autor indicado.
    """
    # TODO: Implementa la función
    pass


def libros_de_autor(nombre_autor):
    """
    Devuelve un QuerySet con los libros del autor cuyo nombre se indica.
    Si el autor no existe, el QuerySet estará vacío.
    """
    # TODO: Implementa la consulta
    pass


def actualizar_anio(titulo, nuevo_anio):
    """
    Actualiza el año del libro con ese título y devuelve el libro actualizado.
    Si el libro no existe, devuelve None.
    """
    # TODO: Implementa la función
    pass


def eliminar_libro(titulo):
    """
    Elimina el libro con ese título y devuelve el número de libros eliminados.
    """
    # TODO: Implementa la función
    pass
