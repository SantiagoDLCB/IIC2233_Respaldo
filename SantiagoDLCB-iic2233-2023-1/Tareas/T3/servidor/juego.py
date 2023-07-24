from collections import deque
import json
import os
import random
from threading import Event
import time

from Scripts.funciones import imprimir_logs
from Scripts.clases import Jugador, Status
with open(os.path.join('parametros.json')) as archivo:
    PARAMETROS = json.load(archivo)


class Juego:
    evento_reiniciar_tiempo = Event()

    def __init__(self, padre, jugadores: deque):
        self.padre = padre
        self.turno_actual: Jugador = Jugador(*PARAMETROS["JUGADOR_NULO"])
        self.jugadores: deque(Jugador) = jugadores
        self.__valor = PARAMETROS["VALOR_INICIAL"]
        self.turno_anterior: Jugador = Jugador(*PARAMETROS["JUGADOR_NULO"])
        self.__numero_turno = PARAMETROS["TURNO_INICIAL"]
        self.cambio_dados = PARAMETROS["CAMBIO_DADOS_INICIAL"]
        self.paso = PARAMETROS["PASO_INICIAL"]
        self.jugando = False
        self.see = PARAMETROS["CLIENTES_SEE_INICIAL"]

    @property
    def valor(self) -> int:
        return self.__valor

    @valor.setter
    def valor(self, nuevo_num):
        self.__valor = nuevo_num
        if nuevo_num == 0:
            self.numero_turno = 1
        else:
            self.numero_turno += 1

    @property
    def numero_turno(self) -> int:
        return self.__numero_turno

    @numero_turno.setter
    def numero_turno(self, nuevo_num):
        self.cambio_dados = False
        self.paso -= 1
        if nuevo_num != 1:
            self.turno_anterior = self.jugadores[-1]
            self.turno_actual = self.jugadores[0]
        else:
            self.turno_anterior = Jugador(*PARAMETROS["JUGADOR_NULO"])
            self.turno_actual = self.jugadores[0]
            self.tirar_dados_todos()
        imprimir_logs(PARAMETROS["LOG_INICIO_TURNO"], self.turno_actual.id)
        self.__numero_turno = nuevo_num
        self.evento_reiniciar_tiempo.set()
        if self.turno_actual.bot:
            self.jugar_bot()

    def obtener_status(self) -> Status:
        return Status(self.turno_actual.id, self.valor,
                      self.turno_anterior.id, self.numero_turno)

    def ejecutar_accion(self, emisor, operacion, datos,
                        id_jugadores_reales) -> None:
        detalles = '-'
        if operacion == PARAMETROS["COMENZAR_JUEGO"] and not self.jugando:
            self.jugando = True
            self.crear_jugadores(id_jugadores_reales)
            detalles = PARAMETROS["DETALLES_COMENZAR"] + \
                PARAMETROS["SEPARADOR_DETALLES"].join(
                (x.id for x in self.jugadores))
            imprimir_logs(operacion, emisor, detalles)
            imprimir_logs(
                PARAMETROS["LOG_INICIO_TURNO"], self.turno_actual.id)
        elif operacion == PARAMETROS["ANUNCIAR_VALOR"]:
            self.anunciar_valor(emisor, datos)
        elif operacion == PARAMETROS["PASAR_TURNO"]:
            self.pasar_turno(emisor)
        elif operacion == PARAMETROS["CAMBIAR_DADOS"]:
            self.cambiar_dados(emisor)
        elif operacion == PARAMETROS["USAR_PODER"]:
            self.usar_poder(emisor, datos)
        elif operacion == PARAMETROS["DUDAR"]:
            self.dudar(emisor)
        elif operacion == PARAMETROS["SEE"]:
            self.see.append(emisor)

    def crear_jugadores(self, lista_jugadores: list) -> None:
        bots = []
        for n in range(PARAMETROS["NUMERO_JUGADORES"]-len(lista_jugadores)):
            id_bot = PARAMETROS["BOT_ID"]+str(n+1)
            bots.append(id_bot)
        todos = lista_jugadores+bots
        random.shuffle(todos)
        jugadores_estado_inicial = deque()
        for jugador_id in todos:
            jugador_nuevo = Jugador(jugador_id, PARAMETROS["NUMERO_VIDAS"],
                                    *PARAMETROS["JUGADOR_NULO"][2:],
                                    jugador_id in bots)
            jugadores_estado_inicial.append(jugador_nuevo)
        self.jugadores: deque[Jugador] = jugadores_estado_inicial
        self.tirar_dados_todos()
        self.turno_actual = self.jugadores[0]
        self.turno_anterior = Jugador(*PARAMETROS["JUGADOR_NULO"])

    def tirar_dados_todos(self) -> None:
        for jugador in self.jugadores:
            jugador.tirar_dados()

    def anunciar_valor(self, emisor, valor: str) -> None:
        valor = str(valor)
        if emisor != self.turno_actual.id:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_TURNO"], emisor)
        elif valor.isnumeric():
            if PARAMETROS["VALOR_MAXIMO"] >= int(valor) > self.valor:
                self.cronometro = False
                detalles = PARAMETROS["DETALLES_ANUNCIAR"] + valor
                imprimir_logs(PARAMETROS["ANUNCIAR_VALOR"], emisor, detalles)
                self.ordenar_cola(self.jugadores[1].id)
                self.valor = int(valor)
            elif int(valor) > PARAMETROS["VALOR_MAXIMO"]:
                self.padre.enviar_error_juego(
                    PARAMETROS["ERROR_ANUNCIAR_IMPOSIBLE"], emisor)
            else:
                self.padre.enviar_error_juego(
                    PARAMETROS["ERROR_ANUNCIAR_MENOR"], emisor)

        else:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_NUMERO"], emisor)

    def pasar_turno(self, emisor) -> None:
        if emisor != self.turno_actual.id:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_TURNO"], emisor)
        else:
            imprimir_logs(PARAMETROS["PASAR_TURNO"], emisor)
            self.cronometro = False
            self.ordenar_cola(self.jugadores[1].id)
            self.paso = 2
            self.numero_turno += 1

    def cambiar_dados(self, emisor) -> None:
        if emisor != self.turno_actual.id:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_TURNO"], emisor)
        elif self.cambio_dados:
            self.padre.enviar_error_juego(
                PARAMETROS["ERROR_CAMBIAR_DOBLE"], emisor)
        else:
            imprimir_logs(PARAMETROS["CAMBIAR_DADOS"], emisor)
            self.turno_actual.tirar_dados()
            self.cambio_dados = True

    def usar_poder(self, emisor,  objetivo: dict) -> None:
        nombres = [x.id for x in self.jugadores]
        dado1 = self.turno_actual.dado1
        dado2 = self.turno_actual.dado2
        combinaciones = [[dado1, dado2], [dado2, dado1]]
        if emisor != self.turno_actual.id:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_TURNO"], emisor)
        elif objetivo not in nombres:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_JUGADOR_INVALIDO"],
                                          emisor)
        elif PARAMETROS["COMBINACION_ATAQUE"] in combinaciones:
            if emisor == objetivo:
                self.padre.enviar_error_juego(
                    PARAMETROS["ERROR_JUGADOR_INVALIDO"], emisor)
                return
            self.cronometro = False
            self.padre.actualizar_juego_clientes(
                dudo=False, emisor_poder=emisor)
            time.sleep(PARAMETROS["TIEMPO_DUDAR"])
            indice_jug = nombres.index(objetivo)
            detalles = PARAMETROS["DETALLES_ATAQUE"] + objetivo
            imprimir_logs(PARAMETROS["USAR_PODER"], emisor, detalles)
            self.jugadores[indice_jug].vida -= 1
            self.ordenar_cola(objetivo)
            self.analizar_perder()
            self.valor = 0
        elif PARAMETROS["COMBINACION_TERREMOTO"] in combinaciones:

            self.cronometro = False
            self.padre.actualizar_juego_clientes(
                dudo=False, emisor_poder=emisor)
            time.sleep(PARAMETROS["TIEMPO_DUDAR"])
            indice_jug = nombres.index(objetivo)
            vida_nueva = random.randint(1, PARAMETROS['NUMERO_VIDAS'])
            detalles = PARAMETROS["DETALLES_TERREMOTO"] + objetivo
            imprimir_logs(PARAMETROS["USAR_PODER"], emisor, detalles)
            self.jugadores[indice_jug].vida = vida_nueva
            self.ordenar_cola(self.jugadores[1].id)
            self.valor = 0
        else:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_PODER"], emisor)

    def dudar(self, emisor) -> None:
        if emisor != self.turno_actual.id:
            self.padre.enviar_error_juego(PARAMETROS["ERROR_TURNO"], emisor)
        elif self.cambio_dados:
            self.padre.enviar_error_juego(
                PARAMETROS["ERROR_DUDAR_CAMBIAR"], emisor)
        elif self.turno_anterior.id is None:
            self.padre.enviar_error_juego(
                PARAMETROS["ERROR_DUDAR_TURNO"], emisor)
        else:
            self.cronometro = False
            imprimir_logs(PARAMETROS["DUDAR"], emisor)
            self.padre.actualizar_juego_clientes(dudo=True)
            time.sleep(PARAMETROS["TIEMPO_DUDAR"])
            anterior = self.turno_anterior
            valor_real = anterior.dado1 + anterior.dado2
            if ((self.paso == 1 and valor_real != PARAMETROS["VALOR_PASO"]) or
                    (valor_real < self.valor and self.paso != 1)):
                anterior.vida -= 1
                self.ordenar_cola(self.jugadores[-1].id)
                self.analizar_perder()
                self.valor = 0
            else:
                self.turno_actual.vida -= 1
                self.analizar_perder()
                self.valor = 0

    def ordenar_cola(self, primero) -> None:
        while self.jugadores[0].id != primero:
            jugador1 = self.jugadores.popleft()
            self.jugadores.append(jugador1)

    def jugar_bot(self) -> None:
        self.padre.actualizar_juego_clientes()
        time.sleep(PARAMETROS["TIEMPO_INICIO_BOT"])
        if (self.turno_anterior.id is not None and
                random.random() < PARAMETROS["PROB_DUDAR"]):
            self.dudar(self.turno_actual.id)
        else:
            self.cambiar_dados(self.turno_actual)
            time.sleep(PARAMETROS["TIEMPO_ACCION_BOT"])
            if (random.random() < PARAMETROS["PROB_ANUNCIAR"]
                    and self.valor < PARAMETROS["VALOR_MAXIMO"]):
                valor_anunciar = random.randint(
                    1+self.valor, PARAMETROS["VALOR_MAXIMO"])
                if valor_anunciar < PARAMETROS["VALOR_MAXIMO"]:
                    self.anunciar_valor(
                        self.turno_actual.id, valor_anunciar)
                else:
                    self.pasar_turno(self.turno_actual.id)
            else:
                self.pasar_turno(self.turno_actual.id)
        self.padre.actualizar_juego_clientes()

    def analizar_perder(self, desconectado=False) -> None:
        for jugador in self.jugadores:
            if jugador.vida == 0:
                self.ordenar_cola(jugador.id)
                self.jugadores.popleft()
                if not jugador.bot and not desconectado:
                    self.padre.finalizar_cliente(
                        jugador.id, PARAMETROS["PERDER"])
            break
        c = 0
        for jugador in self.jugadores:
            if not jugador.bot:
                c += 1
        if len(self.jugadores) == 1:
            self.cronometro = False
            self.evento_reiniciar_tiempo.set()
            self.activo_correr_tiempo = False
            imprimir_logs(PARAMETROS["LOG_TERMINAR"],
                          detalles=PARAMETROS["DETALLES_GANADOR"] +
                          self.jugadores[0].id)
            if c == 1:
                self.padre.finalizar_cliente(self.jugadores[0].id,
                                             PARAMETROS["GANAR"])
            self.padre.ciclo_aceptar_conexiones = False
            time.sleep(PARAMETROS["TIEMPO_DUDAR"])
            os._exit(0)

    def correr_tiempo(self) -> None:
        t = PARAMETROS["TIEMPO_TURNO"]
        self.activo_correr_tiempo = True
        self.cronometro = True
        self.padre.enviar_tiempo(t)
        while self.activo_correr_tiempo:
            self.evento_reiniciar_tiempo.clear()
            t = PARAMETROS["TIEMPO_TURNO"]
            self.cronometro = True
            self.padre.enviar_tiempo(t)
            while t != 0 and self.cronometro:
                time.sleep(PARAMETROS["TIEMPO_SECS"])
                t -= 1
                self.padre.enviar_tiempo(t)
            if t == 0:
                self.turno_actual.vida -= 1
                self.analizar_perder()
                self.valor = 0
                self.padre.actualizar_juego_clientes()
            self.evento_reiniciar_tiempo.wait()
