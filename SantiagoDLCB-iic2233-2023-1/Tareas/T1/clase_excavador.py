from parametros import (FELICIDAD_ADICIONAL_DOCENCIO,
                        FUERZA_ADICIONAL_DOCENCIO, ENERGIA_PERDIDA_DOCENCIO,
                        ENERGIA_ADICIONAL_TAREO, SUERTE_ADICIONAL_TAREO,
                        EDAD_ADICIONAL_TAREO, FELICIDAD_PERDIDA_TAREO,
                        PROB_ENCONTRAR_ITEM, PROB_ENCONTRAR_TESORO,
                        PROB_ENCONTRAR_CONSUMIBLE)
import random
from clase_item import Consumible, Tesoro
from clase_arena import Arena


class Excavador:
    def __init__(self, nombre: str, edad: int, energia: int, fuerza: int,
                 suerte: int, felicidad: int, *args, **kwargs):
        self.nombre = nombre
        self.tipo = ''
        self.__edad = edad
        self.__energia = energia
        self.__fuerza = fuerza
        self.__suerte = suerte
        self.__felicidad = felicidad
        self.descanso_restante = 0
        # corrige atributos al inicializar con los getter y setter
        self.edad = self.edad
        self.energia = self.energia
        self.fuerza = self.fuerza
        self.suerte = self.suerte
        self.felicidad = self.felicidad

    @property
    def edad(self) -> int:
        return self.__edad

    @edad.setter
    def edad(self, nueva_edad: int):
        if nueva_edad < 18:
            self.__edad = 18
        elif nueva_edad > 60:
            self.__edad = 60
        else:
            self.__edad = int(nueva_edad)

    @property
    def energia(self) -> int:
        return self.__energia

    @energia.setter
    def energia(self, nueva_energia: int) -> None:
        if nueva_energia < 20 and self.tipo == 'hibrido':
            self.__energia = 20
        elif nueva_energia <= 0:
            self.__energia = 0
            self.descansar()  # REVISAR
        elif nueva_energia > 100:
            self.__energia = 100
        else:
            self.__energia = int(nueva_energia)

    @property
    def fuerza(self) -> int:
        return self.__fuerza

    @fuerza.setter
    def fuerza(self, nueva_fuerza: int):
        if nueva_fuerza <= 1:
            self.__fuerza = 1
        elif nueva_fuerza >= 10:
            self.__fuerza = 10
        else:
            self.__fuerza = int(nueva_fuerza)

    @property
    def suerte(self) -> int:
        return self.__suerte

    @suerte.setter
    def suerte(self, nueva_suerte: int):
        if nueva_suerte < 1:
            self.__suerte = 1
        elif nueva_suerte > 10:
            self.__suerte = 10
        else:
            self.__suerte = int(nueva_suerte)

    @property
    def felicidad(self) -> int:
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad: int):
        if nueva_felicidad < 1:
            self.__felicidad = 1
        elif nueva_felicidad > 10:
            self.__felicidad = 10
        else:
            self.__felicidad = int(nueva_felicidad)

    def cavar(self, Arena1: Arena) -> float:
        dificultad = Arena1.dificultad_arena
        metros_cavados = ((30/self.edad)+(self.felicidad +
                          (2*self.fuerza) / 10)) * (1 / (10*dificultad))
        metros_cavados = round(metros_cavados, 2)
        return metros_cavados

    def descansar(self) -> None:
        dias_descanso = int(self.edad/20)
        self.descanso_restante = dias_descanso
        self.energia = 100

    def encontrar_item(self, Arena_actual):
        probabilidad_item = PROB_ENCONTRAR_ITEM*(self.suerte/10)
        tipos = [Tesoro, Consumible]
        pesos = [PROB_ENCONTRAR_TESORO, PROB_ENCONTRAR_CONSUMIBLE]
        if Arena_actual.tipo in ['mojada', 'magnetica']:
            tipo_random = random.choice(tipos)
        elif random.random() < probabilidad_item:
            tipo_random = random.choices(tipos, pesos, k=1)[0]
        else:
            return None
        items_del_tipo = [item for item in Arena_actual.items
                          if type(item) == tipo_random]
        return random.choice(items_del_tipo)

    def gastar_energia(self):
        energia_gastada = int((10/self.fuerza)+(self.edad/6))
        self.energia -= energia_gastada

    def consumir(self, Consumible1: Consumible):
        self.energia += Consumible1.energia
        self.fuerza += Consumible1.fuerza
        self.suerte += Consumible1.suerte
        self.felicidad += Consumible1.felicidad


class ExcavadorDocencio(Excavador):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'docencio'

    def cavar(self, Arena1: Arena) -> float:
        metros_cavados = super().cavar(Arena1)
        self.felicidad += FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += FUERZA_ADICIONAL_DOCENCIO
        return metros_cavados

    def gastar_energia(self):
        super().gastar_energia()
        self.energia -= ENERGIA_PERDIDA_DOCENCIO


class ExcavadorTareo(Excavador):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'tareo'

    def consumir(self, Consumible1):
        super().consumir(Consumible1)
        self.energia += ENERGIA_ADICIONAL_TAREO
        self.suerte += SUERTE_ADICIONAL_TAREO
        self.edad += EDAD_ADICIONAL_TAREO
        self.felicidad -= FELICIDAD_PERDIDA_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo, Excavador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'hibrido'

    def gastar_energia(self):
        energia_inicial = self.energia
        ExcavadorDocencio.gastar_energia(self)
        energia_perdida = energia_inicial - self.energia
        self.energia = energia_inicial - energia_perdida/2


def crear_excavador_tipo(tipo: str, datos) -> Excavador:
    # Recibe los datos de un item y su respectivo tipo
    # Retorna la instacia respectiva del item y su tipo
    if tipo == 'docencio':
        return ExcavadorDocencio(*datos)
    elif tipo == 'tareo':
        return ExcavadorTareo(*datos)
    elif tipo == 'hibrido':
        return ExcavadorHibrido(*datos)


def obtener_excavadores() -> list:
    # Obtiene la info de los excavadores en excavadores.csv, se cargaran
    # los datos de cada excavador y crea su instacia con crear_excavador_tipo
    # Retorna listado con todos los excavadores instanciados
    with open('excavadores.csv', encoding='utf-8') as archivo:
        datos_excavadores = [linea.strip('\n').split(',')
                             for linea in archivo.readlines()][1:]
    excavadores = []
    for excavador in datos_excavadores:
        datos = [excavador[0]]+[int(elemento) for elemento in excavador[2:]]
        excavadores.append(crear_excavador_tipo(excavador[1], datos))
    return excavadores


def excavadores_inicial_random(cantidad: int) -> list:
    # Recibe una cantidad de excavadores
    # Retorna una lista de largo pedido con excavadores randoms instanciados
    excavadores = obtener_excavadores()
    excavadores_random = random.sample(excavadores, k=cantidad)
    return excavadores_random


def nuevo_excavador(TorneoActual, tipo: str) -> Excavador:
    # Recibe el Torneo y un tipo de excavador
    # Retorna un excavador random del tipo pedido no presente en el Torneo
    excavadores = obtener_excavadores()
    posibles_excavadores = []
    equipo = [excavador.nombre for excavador in TorneoActual.equipo]
    for Posible in excavadores:
        if Posible.nombre not in equipo and Posible.tipo == tipo:
            posibles_excavadores.append(Posible)
    if posibles_excavadores == []:
        return None
    else:
        return random.choice(posibles_excavadores)


if __name__ == "__main__":
    print(*excavadores_inicial_random(2), sep='\n')
    E1 = Excavador('Pepito', 18, 5, 4, 3, 4)
    print(E1.energia)
    E1.energia -= 4
    print(E1.energia)
    E1.energia -= 5
    print(E1.energia)
    E1.energia += 15
    print(E1.energia)
    Eh = ExcavadorHibrido('Pepito', 18, 30, 4, 3, 4)
    Eh.energia -= 15
    print(Eh.energia)  # 20

    Ed = ExcavadorDocencio('doce', 18, 30, 4, 3, 4)
    Ed.energia -= 15
    print(Ed.energia)  # 15

    Et = ExcavadorTareo('doce', 18, 30, 4, 3, 4)
    Et.energia -= 15
    print(Et.energia)  # 15
