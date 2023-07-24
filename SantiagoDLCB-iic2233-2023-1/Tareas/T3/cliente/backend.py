
import json
import os
import pickle
from socket import socket, AF_INET, SOCK_STREAM
import sys
from threading import Lock, Thread

from PyQt5.QtCore import pyqtSignal, QObject
from Scripts.clases import Mensaje, Jugador, Status
from Scripts.cripto import encriptar, desencriptar
from Scripts.codificacion import codificar_mensaje, decodificar_mensaje

with open(os.path.join('parametros.json')) as parametros:
    PARAMETROS = json.load(parametros)


class Backend(QObject):
    lock_serializar_mensaje = Lock()
    lock_enviar_mensaje = Lock()
    lock_deserializar_mensaje = Lock()
    senal_actualizar_cola = pyqtSignal(bool)
    senal_esconder_cola = pyqtSignal()
    senal_actualizar_jugadores = pyqtSignal(list)
    senal_cambiar_ventana = pyqtSignal(list)
    senal_actualizar_datos = pyqtSignal(list)
    senal_actualizar_juego = pyqtSignal(list)
    senal_error_juego = pyqtSignal(str)
    senal_perder = pyqtSignal()
    senal_ganar = pyqtSignal()
    senal_servidor_desconectado = pyqtSignal()
    senal_actualizar_tiempo = pyqtSignal(int)

    def __init__(self, port, host, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conectado = False
        self.cola = True
        self.port = port
        self.host = host
        self.socket_cliente = socket(AF_INET, SOCK_STREAM)
        self.id = PARAMETROS["DEFAULT_ID"]

    def conectar_servidor(self) -> None:
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
        except (ConnectionError, ConnectionAbortedError,
                ConnectionResetError, KeyboardInterrupt):
            self.socket_cliente.close()
            self.conectado = False
            print(PARAMETROS["ERROR_CONECTAR"])
            sys.exit()
        self.escuchando_servidor_thread = Thread(
            target=self.escuchar_servidor_thread,
            daemon=True)
        self.escuchando_servidor_thread.start()

    def enviar_mensaje(self, mensaje_servidor: Mensaje) -> None:
        with self.lock_serializar_mensaje:
            serializado = pickle.dumps(mensaje_servidor)
        encriptado = encriptar(bytearray(serializado),
                               PARAMETROS["N_PONDERADOR"])
        codificado = codificar_mensaje(encriptado)
        with self.lock_enviar_mensaje:
            self.socket_cliente.sendall(codificado)

    def recibir_mensaje(self, mensaje_codificado: bytearray) -> None:
        decodificado = decodificar_mensaje(mensaje_codificado)
        desencriptado = desencriptar(decodificado, PARAMETROS["N_PONDERADOR"])
        with self.lock_deserializar_mensaje:
            deserializado = pickle.loads(desencriptado)
        self.procesar_mensaje(deserializado)

    def escuchar_servidor_thread(self) -> None:
        while self.conectado:
            try:
                mensaje_servidor = bytearray(
                    self.socket_cliente.recv(PARAMETROS["SOCKET_RECV"]))
                self.recibir_mensaje(mensaje_servidor)
            except (ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, KeyboardInterrupt):
                self.senal_servidor_desconectado.emit()
                break

    def procesar_mensaje(self, mensaje: Mensaje) -> None:
        if mensaje.operacion == PARAMETROS["ACTUALIZAR_COLA"]:
            if self.id == "":
                self.id = mensaje.datos[0][-1]
            self.senal_actualizar_jugadores.emit(mensaje.datos[1])
            self.senal_actualizar_cola.emit(mensaje.datos[2])
        elif mensaje.operacion == PARAMETROS["ACTUALIZAR_JUGADORES"]:
            self.senal_esconder_cola.emit()
            if self.cola:
                self.id = mensaje.datos[-1]
                self.cola = False
            self.senal_actualizar_jugadores.emit(mensaje.datos)
        elif mensaje.operacion == PARAMETROS["COMENZAR_JUEGO"]:
            self.senal_cambiar_ventana.emit(mensaje.datos)
        elif mensaje.operacion == PARAMETROS["ACTUALIZAR_JUEGO"]:
            self.senal_actualizar_juego.emit(mensaje.datos)
        elif mensaje.operacion == PARAMETROS["ERROR_JUEGO"]:
            self.senal_error_juego.emit(mensaje.datos)
        elif mensaje.operacion == PARAMETROS["PERDER"]:
            self.conectado = False
            self.socket_cliente.close()
            self.senal_perder.emit()
        elif mensaje.operacion == PARAMETROS["GANAR"]:
            self.conectado = False
            self.socket_cliente.close()
            self.senal_ganar.emit()
        elif mensaje.operacion == PARAMETROS["TIEMPO"]:
            self.senal_actualizar_tiempo.emit(mensaje.datos)

    def enviar_comenzar_juego(self) -> None:
        mensaje = Mensaje(PARAMETROS["COMENZAR_JUEGO"])
        self.enviar_mensaje(mensaje)

    def anunciar_valor(self, valor: str) -> None:
        mensaje = Mensaje(PARAMETROS["ANUNCIAR_VALOR"], valor)
        self.enviar_mensaje(mensaje)

    def pasar_turno(self) -> None:
        mensaje = Mensaje(PARAMETROS["PASAR_TURNO"])
        self.enviar_mensaje(mensaje)

    def cambiar_dados(self) -> None:
        mensaje = Mensaje(PARAMETROS["CAMBIAR_DADOS"])
        self.enviar_mensaje(mensaje)

    def usar_poder(self, objetivo) -> None:
        mensaje = Mensaje(PARAMETROS["USAR_PODER"], objetivo)
        self.enviar_mensaje(mensaje)

    def dudar(self) -> None:
        mensaje = Mensaje(PARAMETROS["DUDAR"])
        self.enviar_mensaje(mensaje)

    def see(self) -> None:
        mensaje = Mensaje(PARAMETROS["SEE"])
        self.enviar_mensaje(mensaje)
