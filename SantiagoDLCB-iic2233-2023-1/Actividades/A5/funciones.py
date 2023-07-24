from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    # TODO: Completar
    with open(ruta) as archivo:
        info = [x.strip('\n').split(",") for x in archivo.readlines()[1:]]
    for x in info:
        yield Producto(int(x[0]), x[1], int(x[2]), x[3], int(x[4]), x[5])


def cargar_categorias(ruta: str) -> Generator:
    # TODO: Completar
    with open(ruta) as archivo:
        info = [x.strip('\n').split(",") for x in archivo.readlines()[1:]]
    for x in info:
        yield Categoria(x[0], int(x[1]))

    pass


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_productos(generador_productos: Generator) -> map:
    # TODO: Completar
    return map(lambda producto: producto.nombre, generador_productos)


def obtener_precio_promedio(generador_productos: Generator) -> int:
    g1, g2 = duplicador_generadores(generador_productos)
    suma = reduce(lambda x, y: x.precio+y.precio, g1)

    largo = reduce(lambda x, y: x + 1, [1], 1)
    return int(suma / largo)


def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    # TODO: Completar
    return filter(lambda x: True if (x.unidad_medida == unidad and
                                     medida_min <= x.medida <= medida_max) else False,
                  generador_productos)


def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> Generator:
    # TODO: Completar
    filtro1 = filter(lambda x: x.nombre_categoria == nombre_categoria,
                     generador_categorias)
    map1 = map(lambda x: x.id_producto, filtro1)
    lista = generador_a_lista(map1)
    return filter(lambda x:  x.id_producto in lista, generador_productos)


def agrupar_por_pasillo(generador_productos: Generator) -> Generator:
    # TODO: Completar

    return groupby(generador_productos, lambda x: x.pasillo)


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        # TODO: Completar
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)

    def __iter__(self):
        # TODO: Completar
        return self

    def __next__(self):
        if len(self.productos_iterable) == 0:
            raise StopIteration()
        else:
            minimo = min(self.productos_iterable, key=lambda x: x.precio)
            self.productos_iterable.remove(minimo)
            return minimo
