from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import parametros as p
import os
from copy import deepcopy
from backend.entidades import (Entidad, Luigi, FantasmaHorizontal,
                               FantasmaVertical, FollowerVillain)
from backend.funciones import generar_mapa_vacio


class Logica(QObject):
    # senales inicio
    senal_modo_constructor = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_error_nombre = pyqtSignal(str)
    # senales juego
    senal_actualizar_vidas = pyqtSignal(int)
    senal_actualizar_temporizador = pyqtSignal(int)
    senal_actualizar_obj_restantes = pyqtSignal(dict)
    senal_error_drop = pyqtSignal(str)
    senal_reiniciar_mapa = pyqtSignal(bool)
    senal_crear_entidad = pyqtSignal(str, int, int, int)
    senal_crear_bloque = pyqtSignal(str, int, int)
    senal_mover_entidad = pyqtSignal(int, str, int)
    senal_mover_roca = pyqtSignal(int, int, int, int)
    senal_eliminar_entidad = pyqtSignal(int)
    senal_perder = pyqtSignal(str, str)
    senal_ganar = pyqtSignal(str, float)
    luigi_caminando = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inf_status = False
        self.__vida = p.CANTIDAD_VIDAS
        self.vida = self.vida
        self.mapa = generar_mapa_vacio()
        self.entidades = {}
        self.luigi = Luigi(self, -32, -32)
        self.luigi.id = -1
        self.pausado = False
        self.tiempo = p.TIEMPO_CUENTA_REGRESIVA
        self.objetos_restantes = deepcopy(p.DICT_MAXIMO_OBJETOS)
        self.timer_temporizador = QTimer(self)
        self.timer_temporizador.setInterval(1000)
        self.timer_temporizador.timeout.connect(self.temporizador)

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, nueva_vida):
        """Actualiza la vida y reinicia en caso de que esta disminuya.
        Tambien manda la senal de perder en caso de que no queden vidas"""
        if nueva_vida < self.vida:
            self.reiniciar_nivel()

        if self.inf_status is False:
            self.__vida = nueva_vida
            self.senal_actualizar_vidas.emit(self.__vida)
            if nueva_vida == 0:
                self.senal_perder.emit(self.nombre, p.MENSAJE_PERDER_VIDAS)

    def intentar_login(self, nombre: str, mapa_elegido: str):
        """Prueba si es posible hacer login con los datos entregados"""
        n = len(nombre)
        if (nombre != '' and nombre.isalnum() is True and n >= p.MIN_CARACTERES
                and n <= p.MAX_CARACTERES):
            print(nombre)
            self.nombre = nombre
            if mapa_elegido == p.MODO_CONSTRUCTOR:
                self.senal_modo_constructor.emit()
            else:
                with open(os.path.join(
                        *p.PATH_CARPETA_MAPAS, mapa_elegido)) as arch:
                    mapa = [list(x.strip('\n')) for x in arch.readlines()]
                self.senal_iniciar_juego.emit()
                self.timer_temporizador.start()
                self.mapa = mapa
                self.reiniciar_nivel()
        else:
            if nombre == '':
                error = p.MENSAJE_ERROR_NOMBRE_VACIO
            elif not nombre.isalnum():
                error = p.MENSAJE_ERROR_NOMBRE_ALFANUM
            elif n > p.MAX_CARACTERES:
                error = p.MENSAJE_ERROR_NOMBRE_MAX + str(p.MAX_CARACTERES)
            elif n < p.MIN_CARACTERES:
                error = p.MENSAJE_ERROR_NOMBRE_MIN + str(p.MIN_CARACTERES)
            self.senal_error_nombre.emit(error)

    def temporizador(self):
        """Lleva el tiempo actual de la partida y notifica al frontend
        en caso de terminarse"""
        self.tiempo -= 1
        self.senal_actualizar_temporizador.emit(self.tiempo)
        if self.tiempo == 0:
            self.senal_perder.emit(self.nombre, p.MENSAJE_PERDER_TIEMPO)

    def reiniciar_nivel(self):
        """Elimina las entidades del nivel actual y
        manda una senal para que el frontend tambien lo haga"""
        Entidad.id_general = 0
        while self.entidades != {}:
            id = list(self.entidades.keys())[0]
            self.entidades[id].morir()
        self.senal_reiniciar_mapa.emit(False)

    def recargar_nivel(self):
        """Vuelve a cargar el nivel actual"""
        self.cargar_ubic_bloques(self.mapa)
        self.cargar_mapa(self.mapa)
        self.play_fantasmas()

    def cargar_mapa_constructor(self):
        """Carga el mapa en el modo constructor sin inicializar
        los movimientos"""
        self.cargar_ubic_bloques(self.mapa)
        self.cargar_mapa(self.mapa)

    def limpiar_constructor(self):
        """Realiza la accion de limpiar el modo cosntructor y
        mandar las senales para actualizar dichos cambios al frontend"""
        self.mapa = generar_mapa_vacio()
        Entidad.id_general = 0
        while self.entidades != {}:
            id = list(self.entidades.keys())[0]
            self.entidades[id].morir()
        self.senal_reiniciar_mapa.emit(True)
        self.objetos_restantes = deepcopy(p.DICT_MAXIMO_OBJETOS)
        self.senal_actualizar_obj_restantes.emit(self.objetos_restantes)
        self.cargar_mapa_constructor()

    def drop_objeto(self, tipo, x, y, en_mapa=True):
        """Recibe el drop de un objeto y lo coloca correctamente,
        para posteriormente actualizar el frontend. Ademas en caso de que
        el drop sea incorrecto,manda una senal al frontend para notificar
        al respecto"""
        x_min = p.PIXELES_CASILLA * (x // p.PIXELES_CASILLA)
        y_min = p.PIXELES_CASILLA * (y//p.PIXELES_CASILLA)
        x_max, y_max = x_min + p.PIXELES_CASILLA, y_min + p.PIXELES_CASILLA
        x_nueva = x_max // p.PIXELES_CASILLA
        if abs(x-x_min) <= abs(x_max-x):
            x_nueva = x_min//p.PIXELES_CASILLA
        y_nueva = y_max // p.PIXELES_CASILLA
        if abs(y-y_min) <= abs(y_max-y):
            y_nueva = y_min//p.PIXELES_CASILLA
        restantes = self.objetos_restantes[tipo]
        if en_mapa and x_nueva not in (0, p.ANCHO_GRILLA-1) and \
                y_nueva not in (0, p.LARGO_GRILLA-1):
            if self.mapa[y_nueva-1][x_nueva-1] == '-' and \
                    restantes > 0:
                self.mapa[y_nueva-1][x_nueva-1] = tipo
                self.objetos_restantes[tipo] -= 1
                self.cargar_mapa_constructor()
                self.senal_actualizar_obj_restantes.emit(
                    self.objetos_restantes)
            elif restantes <= 0:
                self.senal_error_drop.emit(p.MENSAJE_ERROR_DROP_INSUFICIENTES)
            else:
                self.senal_error_drop.emit(p.MENSAJE_ERROR_DROP_TOPE)
        elif en_mapa is False:
            self.senal_error_drop.emit(p.MENSAJE_ERROR_DROP_MAPA)
        else:
            self.senal_error_drop.emit(p.MENSAJE_ERROR_DROP_INCORRECTO)

    def cargar_ubic_bloques(self, mapa):
        """Carga las ubicaciones de los bloques del mapa y
        manda la senal para crearl dichos bloques en el frontend"""
        a = p.ANCHO_GRILLA
        b = p.LARGO_GRILLA
        pixeles = p.PIXELES_CASILLA
        self.paredes = [(x*pixeles, 0) for x in range(0, a-1)] + \
            [(x*pixeles, (b-1)*pixeles) for x in range(0, a-1)] + \
            [(0, y*pixeles) for y in range(0, b-1)] + \
            [((a-1)*pixeles, y*pixeles) for y in range(0, b-1)]
        self.rocas = []
        self.fuegos = []
        self.estrella = []
        bloques = {'P': self.paredes, 'R': self.rocas,
                   'F': self.fuegos, 'S': self.estrella}
        for y in range(len(mapa)):
            for x in range(len(mapa[y])):
                if mapa[y][x] in bloques.keys():
                    bloques[mapa[y][x]].append(
                        ((x+1)*pixeles, (y+1)*pixeles))
                    self.senal_crear_bloque.emit(mapa[y][x], x+1, y+1)

    def cargar_mapa(self, mapa):
        """Carga las entidades del mapa y
        manda la senal para crearlas en el frontend"""
        entidades = {p.LUIGI: Luigi, p.FANTASMA_H: FantasmaHorizontal,
                     p.FANTASMA_V: FantasmaVertical,
                     p.FOLLOWER: FollowerVillain}
        pixeles = p.PIXELES_CASILLA
        for y in range(len(mapa)):
            for x in range(len(mapa[y])):
                if mapa[y][x] == p.LUIGI:
                    self.luigi: Luigi = entidades[mapa[y][x]](
                        self, (x+1)*pixeles, (y+1)*pixeles)
                    self.senal_crear_entidad.emit(
                        mapa[y][x], self.luigi.id, self.luigi.x, self.luigi.y)
                    self.entidades.update({self.luigi.id: self.luigi})
                elif mapa[y][x] in entidades.keys():
                    entidad = entidades[mapa[y][x]](
                        self, (x+1)*pixeles, (y+1)*pixeles)
                    self.entidades.update({entidad.id: entidad})
                    self.senal_crear_entidad.emit(
                        mapa[y][x], entidad.id, entidad.x, entidad.y)

    def play_fantasmas(self):
        """Inicia el movimiento de los fantasmas"""
        for id in self.entidades.keys():
            if id != self.luigi.id:
                self.entidades[id].timer_movimiento.start()

    def capturar_estrella(self):
        """Realiza la accion de capturar la estrella y ganar la partida"""
        if self.inf_status:
            puntaje = p.TIEMPO_CUENTA_REGRESIVA * p.MULTIPLICADOR_PUNTAJE/1

        elif self.inf_status is False:
            puntaje = self.tiempo * p.MULTIPLICADOR_PUNTAJE/1
            puntaje = puntaje/(p.CANTIDAD_VIDAS-self.vida + 1)
        if (self.luigi.x, self.luigi.y) in self.estrella:
            self.senal_ganar.emit(self.nombre, puntaje)

    def tecla(self, direccion: str):
        """Recibe la direccion en que luigi debe moverse y
        en caso de ser posible inicia el proceso"""
        if self.luigi_caminando is False and self.pausado is False:
            self.luigi_caminando = True
            self.luigi.direccion = direccion
            self.luigi.timer_movimiento.start()

    def pausa(self, pausado):
        """Pausa o reanuda la partida dependiendo del status
        recibido de pausado"""
        self.pausado = pausado
        if self.pausado:
            self.timer_temporizador.stop()
            ids = list(self.entidades.keys())
            for id in ids:
                entidad = self.entidades[id]
                entidad.timer_movimiento.stop()
                while entidad.x % p.PIXELES_CASILLA != 0 or \
                        entidad.y % p.PIXELES_CASILLA != 0:
                    entidad.mover()
        else:
            if self.inf_status is False:
                self.timer_temporizador.start()
            ids = list(self.entidades.keys())
            ids.remove(self.luigi.id)
            for id in ids:
                entidad = self.entidades[id]
                entidad.timer_movimiento.start()

    def cheatcode_kil(self):
        """Realiza la accion del cheatcode 1 KIL"""
        ids = list(self.entidades.keys())
        ids.remove(self.luigi.id)
        for id in ids:
            self.entidades[id].morir()

    def cheatcode_inf(self):
        """Realiza la accion del cheatcode 2 INF"""
        self.inf_status = True
        self.timer_temporizador.stop()

    def volver_jugar(self):
        """Reinicia el nivel junto con las vidas y timer"""
        self.inf_status = False
        self.vida = p.CANTIDAD_VIDAS
        self.tiempo = p.TIEMPO_CUENTA_REGRESIVA
        self.senal_actualizar_temporizador.emit(self.tiempo)
        self.pausa(False)
        self.reiniciar_nivel()
