import random
from abc import ABC, abstractmethod
from clase_item import cargar_items
from parametros import POND_ARENA_NORMAL


class Arena(ABC):
    def __init__(self, nombre: str, rareza: int, humedad: int,
                 dureza: int, estatica: int):
        self.nombre = nombre
        self.tipo = ''
        self.__rareza = rareza  # entre 1 y 10
        self.__humedad = humedad  # entre 1 y 10
        self.__dureza = dureza  # entre 1 y 10
        self.__estatica = estatica  # entre 1 y 10
        self.items = cargar_items()
        # corrige atributos al inicializar con los getter y setter
        self.rareza = self.rareza
        self.humedad = self.humedad
        self.dureza = self.dureza
        self.estatica = self.estatica
        # asigna la dificultad con los atributos corregidos
        self.__dificultad_arena = self._calcular_dificultad()

    @property
    def rareza(self):
        return self.__rareza

    @rareza.setter
    def rareza(self, nueva_rareza):
        if nueva_rareza > 10:
            self.__rareza = 10
        elif nueva_rareza < 1:
            self.__rareza = 1
        else:
            self.__rareza = nueva_rareza

    @property
    def humedad(self):
        return self.__humedad

    @humedad.setter
    def humedad(self, nueva_humedad):
        if nueva_humedad > 10:
            self.__humedad = 10
        elif nueva_humedad < 1:
            self.__humedad = 1
        else:
            self.__humedad = nueva_humedad

    @property
    def dureza(self):
        return self.__dureza

    @dureza.setter
    def dureza(self, nueva_dureza):
        if nueva_dureza > 10:
            self.__dureza = 10
        elif nueva_dureza < 1:
            self.__dureza = 1
        else:
            self.__dureza = nueva_dureza

    @property
    def estatica(self):
        return self.__estatica

    @estatica.setter
    def estatica(self, estatica):
        if estatica > 10:
            self.__estatica = 10
        elif estatica < 1:
            self.__estatica = 1
        else:
            self.__estatica = estatica

    @property
    def dificultad_arena(self):
        self.dificultad_arena = self._calcular_dificultad()
        return self.__dificultad_arena

    @dificultad_arena.setter
    def dificultad_arena(self, dificultad_arena):
        self.__dificultad_arena = dificultad_arena

    @abstractmethod
    def _calcular_dificultad(self) -> float:
        pass


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'normal'

    def _calcular_dificultad(self) -> float:
        dificultad = round((self.rareza + self.humedad +
                            self.dureza + self.estatica)/40, 2)
        dificultad *= POND_ARENA_NORMAL
        dificultad = round(dificultad, 2)
        return dificultad


class ArenaMojada(Arena):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'mojada'

    def _calcular_dificultad(self) -> float:
        dificultad = round((self.rareza + self.humedad +
                            self.dureza + self.estatica)/40, 2)
        return dificultad


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'rocosa'

    def _calcular_dificultad(self) -> float:
        dificultad = (self.rareza + self.humedad +
                      (2*self.dureza) + self.estatica) / 50
        dificultad = round(dificultad, 2)
        return dificultad


class ArenaMagnetica(ArenaMojada, ArenaRocosa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'magnetica'

    def _calcular_dificultad(self) -> float:
        dificultad = (self.rareza + self.humedad +
                      (2*self.dureza) + self.estatica) / 50
        dificultad = round(dificultad, 2)
        return dificultad


def crear_arena_tipo(tipo: str, datos: list) -> Arena:
    # Recibe los datos de una arena y su respectivo tipo
    # Retorna la instacia respectiva de la arena y su tipo
    if tipo == 'normal':
        ArenaCreada = ArenaNormal(*datos)
    elif tipo == 'mojada':
        ArenaCreada = ArenaMojada(*datos)
    elif tipo == 'rocosa':
        ArenaCreada = ArenaRocosa(*datos)
    elif tipo == 'magnetica':
        ArenaCreada = ArenaMagnetica(*datos)
    return ArenaCreada


def arena_inicial_random(tipo_arena: str) -> Arena:
    # Recibe un tipo de arena
    # Retorna una arena instanciado del tipo pedido
    with open('arenas.csv', encoding='utf-8') as archivo:
        lista_arenas = [linea.strip('\n').split(',')
                        for linea in archivo.readlines()]
    lista_arenas = [arena for arena in lista_arenas if tipo_arena == arena[1]]
    arena = random.choice(lista_arenas)
    arena = arena[:1] + [int(elemento) for elemento in arena[2:]]
    return crear_arena_tipo(tipo_arena, arena)


if __name__ == '__main__':
    A1 = arena_inicial_random('normal')
    print(A1.nombre, A1.tipo, A1.rareza, A1.humedad,
          A1.dureza, A1.estatica, sep='\n')
    Anormal = ArenaNormal('normal', 1, 1, 2, 1)
    print(Anormal.nombre, Anormal.tipo, Anormal.rareza, Anormal.humedad,
          Anormal.dureza, Anormal.estatica, Anormal.dificultad_arena)
    Amojada = ArenaMojada('mojada', 1, 1, 2, 1)
    print(Amojada.nombre, Amojada.tipo, Amojada.rareza, Amojada.humedad,
          Amojada.dureza, Amojada.estatica, Amojada.dificultad_arena)
    Arocosa = ArenaRocosa('rocosa', 1, 1, 2, 1)
    print(Arocosa.nombre, Arocosa.tipo, Arocosa.rareza, Arocosa.humedad,
          Arocosa.dureza, Arocosa.estatica, Arocosa.dificultad_arena)
    Amagnetica = ArenaMagnetica('magnetica', 1, 1, 2, 1)
    print(Amagnetica.nombre, Amagnetica.tipo, Amagnetica.rareza,
          Amagnetica.humedad, Amagnetica.dureza, Amagnetica.estatica,
          Amagnetica.dificultad_arena)
    Amagnetica.dureza = 10
    print(Amagnetica.nombre, Amagnetica.tipo, Amagnetica.rareza,
          Amagnetica.humedad, Amagnetica.dureza, Amagnetica.estatica,
          Amagnetica.dificultad_arena)
