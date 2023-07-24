from abc import ABC


class Item(ABC):
    def __init__(self, nombre, tipo, descripcion):
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion


class Consumible(Item):
    def __init__(self, energia, fuerza, suerte, felicidad, *args, **kwargs):
        super().__init__(tipo='Consumible', *args, **kwargs)
        self.energia: int = energia
        self.fuerza: int = fuerza
        self.suerte: int = suerte
        self.felicidad: int = felicidad


class Tesoro(Item):
    def __init__(self, calidad: int, cambio: str, *args, **kwargs):
        super().__init__(tipo='Tesoro', *args, **kwargs)
        self.calidad = calidad
        self.cambio = cambio


def crear_item_tipo(tipo: str, datos: list) -> (Consumible | Tesoro):
    # Recibe los datos de un item y su respectivo tipo
    # Retorna la instacia respectiva del item y su tipo
    if tipo == 'Consumible':
        return Consumible(nombre=datos[0], descripcion=datos[1],
                          energia=datos[2], fuerza=datos[3],
                          suerte=datos[4], felicidad=datos[5])
    elif tipo == 'Tesoro':
        return Tesoro(nombre=datos[0], descripcion=datos[1],
                      calidad=datos[2], cambio=datos[3])


def cargar_items() -> list:
    # Lee los archivos que contienen la informacion de los items
    # Carga los datos de cada item y crea su instacia con crear_item_tipo
    # Retorna listado con todos los items instanciado
    items = []
    with open('consumibles.csv', encoding='utf-8') as archivo:
        consumibles = [linea.strip('\n').split(',')
                       for linea in archivo.readlines()][1:]
        for consumible in consumibles:
            datos = consumible[:2] + [int(elemento)
                                      for elemento in consumible[2:]]
            items.append(Consumible(nombre=datos[0], descripcion=datos[1],
                                    energia=datos[2], fuerza=datos[3],
                                    suerte=datos[4], felicidad=datos[5]))
    with open('tesoros.csv', encoding='utf-8') as archivo:
        tesoros = [linea.strip('\n').split(',')
                   for linea in archivo.readlines()][1:]
        for tesoro in tesoros:
            datos = tesoro[:2] + [int(tesoro[2])] + [tesoro[3]]
            items.append(Tesoro(nombre=datos[0], descripcion=datos[1],
                                calidad=datos[2], cambio=datos[3]))
    return items
