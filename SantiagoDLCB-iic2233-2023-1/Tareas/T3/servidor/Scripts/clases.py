import json
import os
import random

from Scripts.funciones import imprimir_logs


with open(os.path.join('parametros.json')) as archivo:
    PARAMETROS = json.load(archivo)


class Mensaje:
    def __init__(self, operacion=None, datos=None):
        self.operacion = operacion
        self.datos = datos


class Jugador:
    def __init__(self, id, vida, dado1, dado2, bot=False):
        self.id = id
        self.__vida = vida
        self.dado1 = dado1
        self.dado2 = dado2
        self.bot = bot

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, nueva_vida):
        detalles = PARAMETROS["DETALLES_VIDA_ANTERIOR"] + \
            str(self.__vida) + \
            PARAMETROS["DETALLES_VIDA_NUEVA"] + str(nueva_vida)
        if nueva_vida < self.__vida:
            imprimir_logs(PARAMETROS["LOG_PIERDE_VIDA"], self.id, detalles)
        elif nueva_vida == self.__vida:
            imprimir_logs(PARAMETROS["LOG_MANTIENE_VIDA"], self.id, detalles)
        else:
            imprimir_logs(PARAMETROS["LOG_CAMBIA_VIDA"], self.id, detalles)
        self.__vida = nueva_vida

    def tirar_dados(self):
        self.dado1 = random.randint(*PARAMETROS["RANGO_DADOS"])
        self.dado2 = random.randint(*PARAMETROS["RANGO_DADOS"])


class Status:
    def __init__(self, turno_actual, num_anunciado, turno_anterior, num_turno):
        self.turno_actual = turno_actual
        self.num_anunciado = num_anunciado
        self.turno_anterior = turno_anterior
        self.num_turno = num_turno
