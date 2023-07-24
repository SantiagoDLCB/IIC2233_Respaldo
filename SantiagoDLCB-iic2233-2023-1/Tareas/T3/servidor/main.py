from collections import deque
import copy
import json
import pickle
import os
from socket import socket, AF_INET, SOCK_STREAM
import sys
from threading import Thread, Lock


from Scripts.funciones import obtener_id_jugador, imprimir_logs
from Scripts.cripto import encriptar, desencriptar
from Scripts.codificacion import codificar_mensaje, decodificar_mensaje
from juego import Juego
from Scripts.clases import Mensaje

with open(os.path.join('parametros.json')) as archivo:
    PARAMETROS = json.load(archivo)


class Servidor:
    lock_serializar_mensaje = Lock()
    lock_enviar_mensaje = Lock()
    lock_deserializar_mensaje = Lock()

    def __init__(self, port: int, host: str):
        self.host = host
        self.port = port
        self.sockets: dict[socket] = {}
        self.id_jugadores = {}
        self.id_cola = {}
        self.sockets_cola = deque()
        self.socket_server = socket(AF_INET, SOCK_STREAM)
        self.bind_listen()
        self.aceptar_conexiones()
        imprimir_logs(*PARAMETROS["TEXTOS_LOGS"])
        self.juego = Juego(self, deque())

    def bind_listen(self) -> None:
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(PARAMETROS["SOCKET_LISTEN"])

    def aceptar_conexiones(self) -> None:
        thread = Thread(target=self.aceptar_conexiones_thread)
        thread.start()

    def aceptar_conexiones_thread(self) -> None:
        """Acepta las conexiones de los clientes y los mete en la sala
        en caso de haber cupos"""
        while True:
            socket_cliente, address = self.socket_server.accept()
            self.sockets[socket_cliente] = address
            self.sockets_cola.append(socket_cliente)
            listening_client_thread = Thread(target=self.listen_client_thread,
                                             args=(socket_cliente, ),
                                             daemon=True)
            listening_client_thread.start()
            self.actualizar_cola(socket_cliente)

            if (len(self.id_jugadores) < PARAMETROS["NUMERO_JUGADORES"] and
                    self.juego.jugadores == deque()):
                self.anadir_cliente_esperando()
                imprimir_logs(PARAMETROS["LOG_CONECTARSE"],
                              self.id_jugadores[socket_cliente])
            else:
                imprimir_logs(PARAMETROS["LOG_CONECTARSE"],
                              self.id_cola[socket_cliente])

    def listen_client_thread(self, socket_cliente: socket) -> None:
        """Escucha activamente al cliente conectado y llama a recibir
        el mensaje en caso de llegar uno"""
        while socket_cliente in self.sockets.keys():
            try:
                mensaje = socket_cliente.recv(PARAMETROS["SOCKET_RECV"])
                if socket_cliente in self.id_jugadores:
                    self.recibir_mensaje(mensaje, socket_cliente)
            except (ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, KeyboardInterrupt):
                self.procedimiento_desconectar(socket_cliente)
                break

    def procedimiento_desconectar(self, socket_cliente, reinicio=True) -> None:
        """Elimina al jugador de todos los registros, llama a su desconexión y
         actualiza al resto de clientes la desconexion """
        if self.juego.jugando:
            self.juego.cronometro = False
        if socket_cliente in self.id_jugadores.keys():
            imprimir_logs(PARAMETROS["LOG_DESCONECTARSE"],
                          self.id_jugadores[socket_cliente])
            id1 = self.id_jugadores[socket_cliente]
            del self.id_jugadores[socket_cliente]
            if self.juego.jugando:
                self.eliminar_jugador_desconectado(id1, reinicio)
        elif socket_cliente in self.sockets_cola:
            imprimir_logs(PARAMETROS["LOG_DESCONECTARSE"],
                          self.id_cola[socket_cliente])
            self.sockets_cola.remove(socket_cliente)
            del self.id_cola[socket_cliente]
            self.actualizar_cola(socket_cliente)
        if socket_cliente in self.sockets.keys():
            del self.sockets[socket_cliente]
        if (len(self.sockets_cola) > 0 and
                len(self.id_jugadores) < PARAMETROS["NUMERO_JUGADORES"]
                and not self.juego.jugando):
            self.anadir_cliente_esperando()
        if self.juego.jugando:
            self.juego.evento_reiniciar_tiempo.set()
        self.actualizar_jugadores(list(self.id_jugadores.values()))

    def anadir_cliente_esperando(self) -> None:
        """Quita de la cola al primer cliente en la cola de espera de la sala y
         lo coloca en la sala, ademas llama a actualiza esa informacion
         al resto de clientes"""
        socket_cliente = self.sockets_cola.popleft()
        id_original = self.id_cola[socket_cliente]
        del self.id_cola[socket_cliente]
        self.actualizar_cola()
        self.id_jugadores[socket_cliente] = id_original
        self.actualizar_jugadores(list(self.id_jugadores.values()))

    def actualizar_cola(self, socket_cliente=None) -> None:
        """Le asigna un nombre al cliente, lo anade a la cola de espera
          de la sala se lo informa a toda la cola para saber su posicion en
          cola y sus nombres"""
        nueva_cola = list(self.id_cola.values())
        jugadores = list(self.id_jugadores.values())
        if socket_cliente is not None:
            usados = nueva_cola + jugadores
            id_nuevo_cliente = obtener_id_jugador(usados)
            nueva_cola.append(id_nuevo_cliente)
            self.id_cola[socket_cliente] = PARAMETROS["DEFAULT_ID"]
            mensaje_cola = Mensaje(PARAMETROS["ACTUALIZAR_COLA"],
                                   [nueva_cola, jugadores, self.juego.jugando])
            self.enviar_mensaje_grupo(mensaje_cola, self.id_cola)
            self.id_cola[socket_cliente] = id_nuevo_cliente
        else:
            mensaje_cola = Mensaje(PARAMETROS["ACTUALIZAR_COLA"],
                                   [nueva_cola, jugadores, self.juego.jugando])
            self.enviar_mensaje_grupo(mensaje_cola, self.id_cola)

    def actualizar_jugadores(self, jugadores) -> None:
        "Actualiza los jugadores en la sala de espera y no en cola"
        mensaje_actualizar_id = Mensaje(
            PARAMETROS["ACTUALIZAR_JUGADORES"], jugadores)
        self.enviar_mensaje_grupo(mensaje_actualizar_id, self.id_jugadores)

    def enviar_mensaje(self, mensaje: Mensaje, socket_cliente: socket) -> None:
        """"Envia un mensaje a un cliente llamando a todo el proceso de
        serializacion,encriptacion y codificacion\n
        (el lock es para que pickle no colapse cuando dos threads
        mandan un mensajes al mismo cliente al mismo tiempo)"""
        with self.lock_serializar_mensaje:
            serializado = pickle.dumps(mensaje)
        encriptado = encriptar(bytearray(serializado),
                               PARAMETROS["N_PONDERADOR"])
        codificado = codificar_mensaje(encriptado)
        try:
            with self.lock_enviar_mensaje:
                socket_cliente.sendall(codificado)
        except (ConnectionError, ConnectionAbortedError,
                ConnectionResetError, KeyboardInterrupt):
            self.procedimiento_desconectar(socket_cliente)

    def enviar_mensaje_grupo(self, mensaje, grupo: dict) -> None:
        """"Envia un mismo mensaje a todos los clientes en un grupo"""
        keys_grupo = list(grupo.keys())
        for socket1 in keys_grupo:
            self.enviar_mensaje(mensaje, socket1)

    def recibir_mensaje(self, mensaje_codificado: bytearray,
                        origen: socket) -> None:
        """Traduce el mensaje, decodificando, desncriptando y deserializando
        para luego llamar a procesar el mensaje\n
        (el lock es para que pickle no colapse cuando dos clientes
        mandan un mensaje al mismo tiempo)"""
        decodificado = decodificar_mensaje(mensaje_codificado)
        if len(decodificado) > 0:
            desencriptado = desencriptar(
                decodificado, PARAMETROS["N_PONDERADOR"])
            with self.lock_deserializar_mensaje:
                mensaje = pickle.loads(desencriptado)
            self.procesar_mensaje(mensaje, origen)

    def procesar_mensaje(self, mensaje: Mensaje, origen):
        """Ejecuta la accion del Mensaje  en el juego para luego actualizar
        lo ocurrido a los clientes. Permite hacer operaciones iniciales
        en caso de comenzar el juego como iniciar el cronometro """
        self.juego.ejecutar_accion(self.id_jugadores[origen],
                                   mensaje.operacion, mensaje.datos,
                                   list(self.id_jugadores.values()))
        if (mensaje.operacion == PARAMETROS["COMENZAR_JUEGO"]):
            self.actualizar_juego_clientes(PARAMETROS["COMENZAR_JUEGO"])
            self.juego.thread_tiempo = Thread(target=self.juego.correr_tiempo,
                                              daemon=True)
            self.juego.thread_tiempo.start()
            if self.juego.turno_actual.bot:
                self.juego.jugar_bot()
            self.actualizar_cola()
        else:
            self.actualizar_juego_clientes()

    def actualizar_juego_clientes(self,
                                  operacion=PARAMETROS["ACTUALIZAR_JUEGO"],
                                  dudo=False, emisor_poder=None) -> None:
        """Actualiza los datos de los jugadores a los clientes. Censura los
        datos en caso de que no pertenezcan al cliente y no este en modo SEE"""
        copia_id_jugadores = list(self.id_jugadores.keys())
        for socket1 in copia_id_jugadores:
            cola = deque()
            for jug in self.juego.jugadores:
                jug2 = copy.deepcopy(jug)
                if (jug2.id != self.id_jugadores[socket1] and not dudo and
                        self.id_jugadores[socket1] not in self.juego.see and
                        jug2.id != emisor_poder):
                    jug2.dado1 = PARAMETROS["DADO_OCULTO"]
                    jug2.dado2 = PARAMETROS["DADO_OCULTO"]
                cola.append(jug2)
            datos = [self.juego.obtener_status(), cola]
            mensaje = Mensaje(operacion, datos)
            self.enviar_mensaje(mensaje, socket1)

    def enviar_error_juego(self, error, jugador) -> None:
        """Envia un Mensaje de Error al jugador especificado"""
        mensaje = Mensaje(PARAMETROS["ERROR_JUEGO"], error)
        copia_id_jugadores = list(self.id_jugadores.keys())
        for socket1 in copia_id_jugadores:
            if self.id_jugadores[socket1] == jugador:
                self.enviar_mensaje(mensaje, socket1)

    def finalizar_cliente(self, jugador, razon) -> None:
        """Envia un mensaje al cliente para que se desconecte
        notificando el motivo"""
        mensaje = Mensaje(razon)
        copia_id_jugadores = list(self.id_jugadores.keys())
        for socket1 in copia_id_jugadores:
            if self.id_jugadores[socket1] == jugador:
                self.enviar_mensaje(mensaje, socket1)
                self.procedimiento_desconectar(socket1, False)

    def eliminar_jugador_desconectado(self, nombre, reinicio) -> None:
        nombres = [x.id for x in self.juego.jugadores]
        """Elimina al Jugador desconectado y realiza el procedimiento
        correspondiente para continuar el juego"""
        if nombre in nombres:
            self.juego.ordenar_cola(nombre)
            self.juego.jugadores.popleft()
            self.juego.analizar_perder(desconectado=True)
            self.actualizar_juego_clientes()
            if reinicio:
                self.juego.valor = 0

    def enviar_tiempo(self, tiempo) -> None:
        """Llama a enviar un mensaje a todos los jugadores actualizando
        el tiempo restante del turno actual"""
        m = Mensaje(PARAMETROS["TIEMPO"], tiempo)
        self.enviar_mensaje_grupo(m, self.id_jugadores)


try:
    server = Servidor(int(sys.argv[1]), PARAMETROS["HOST"])
except IndexError:
    print(PARAMETROS["ERROR_INGRESAR_PUERTO"])
except OSError:
    print(PARAMETROS["ERROR_PUERTO_ACTIVO"])
