"""
Enunciado:
Los QuerySet del ORM de Django permiten construir consultas complejas encadenando
métodos como `filter()`, `exclude()`, `order_by()`, `annotate()` o `aggregate()`,
sin escribir SQL. Además, son perezosos: la consulta no se ejecuta hasta que se
necesitan los datos.

En este ejercicio trabajarás con los pedidos de una tienda. Los modelos `Cliente` y
`Pedido` ya están definidos; tu tarea es implementar las siguientes consultas:

1. `clientes_de_ciudad(ciudad)`: clientes de esa ciudad (sin distinguir mayúsculas
   de minúsculas).
2. `pedidos_pendientes()`: pedidos no pagados, ordenados de mayor a menor importe.
3. `pedidos_caros(minimo)`: pedidos cuyo importe es mayor o igual que `minimo`.
   Debe usar `select_related("cliente")` para evitar consultas adicionales al
   acceder al cliente de cada pedido.
4. `buscar_clientes(texto)`: clientes cuyo nombre **o** email contienen el texto
   (sin distinguir mayúsculas de minúsculas). Debe usar objetos `Q`.
5. `total_gastado(cliente)`: suma de los importes de los pedidos del cliente.
   Si el cliente no tiene pedidos, debe devolver `Decimal("0")`.
6. `ranking_clientes()`: clientes anotados con el número de pedidos en el atributo
   `num_pedidos`, ordenados de más a menos pedidos y, a igualdad, por nombre.
7. `nombres_de_clientes()`: lista con los nombres de los clientes, obtenida con
   `values_list(..., flat=True)`.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test
correspondiente (ej3c2_test.py).
"""

import sys
from decimal import Decimal
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ejercicios.config import configurar_django

configurar_django()

from django.db import models  # noqa: E402
from django.db.models import Count, Q, Sum  # noqa: E402


class Cliente(models.Model):
    """Cliente de la tienda."""

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    ciudad = models.CharField(max_length=60)

    class Meta:
        app_label = "ejercicios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    """Pedido realizado por un cliente."""

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    producto = models.CharField(max_length=100)
    importe = models.DecimalField(max_digits=8, decimal_places=2)
    pagado = models.BooleanField(default=False)

    class Meta:
        app_label = "ejercicios"
        ordering = ["id"]

    def __str__(self):
        return f"{self.producto}: {self.importe} €"


def clientes_de_ciudad(ciudad):
    """
    Devuelve los clientes de la ciudad indicada, sin distinguir mayúsculas.
    """
    # TODO: Implementa la consulta
    pass


def pedidos_pendientes():
    """
    Devuelve los pedidos que todavía no se han pagado, del más caro al más barato.
    """
    # TODO: Implementa la consulta
    pass


def pedidos_caros(minimo):
    """
    Devuelve los pedidos con un importe mayor o igual que `minimo`, cargando
    también el cliente de cada pedido con select_related().
    """
    # TODO: Implementa la consulta
    pass


def buscar_clientes(texto):
    """
    Devuelve los clientes cuyo nombre o email contienen el texto indicado.
    """
    # TODO: Implementa la consulta
    pass


def total_gastado(cliente):
    """
    Devuelve la suma de los importes de los pedidos del cliente.
    """
    # TODO: Implementa la consulta
    pass


def ranking_clientes():
    """
    Devuelve los clientes con el número de pedidos en el atributo `num_pedidos`,
    ordenados de más a menos pedidos y, a igualdad, por nombre.
    """
    # TODO: Implementa la consulta
    pass


def nombres_de_clientes():
    """
    Devuelve una lista con los nombres de todos los clientes.
    """
    # TODO: Implementa la consulta
    pass
