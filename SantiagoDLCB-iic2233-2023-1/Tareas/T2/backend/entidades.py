from PyQt5.QtCore import QObject, QTimer
import random
import parametros as p
from backend.funciones import checkear_tope, checkear_tope_roca, nueva_posicion
from collections import deque


class Entidad(QObject):
    id_general = 0

    def __init__(self, padre, x, y, *args, **kwargs):
        super().__init__(parent=padre, *args, **kwargs)
        self.x = x
        self.y = y
        self.id = Entidad.id_general
        self.padre = padre
        Entidad.id_general += 1
        self.direccion = ""

    def mover(self):
        pixeles = p.PIXELES_MOVER
        if self.direccion == p.UP:
            self.y -= pixeles
        if self.direccion == p.DOWN:
            self.y += pixeles
        if self.direccion == p.LEFT:
            self.x -= pixeles
        if self.direccion == p.RIGHT:
            self.x += pixeles
        self.padre.senal_mover_entidad.emit(
            self.id, self.direccion, pixeles)


class Luigi(Entidad):
    def __init__(self, padre, x, y, *args, **kwargs):
        super().__init__(padre, x, y, *args, **kwargs)
        self.direccion = p.FRONT
        self.timer_movimiento = QTimer(self)
        tiempo_movimiento_luigi = int(1/p.VELOCIDAD_LUIGI)
        self.timer_movimiento.setInterval(tiempo_movimiento_luigi)
        self.timer_movimiento.timeout.connect(self.cambiar_casilla)

    def mover(self):
        super().mover()
        if (self.x, self.y) in self.padre.fuegos:
            self.padre.vida -= 1

    def cambiar_casilla(self):
        x, y, direccion = self.x, self.y, self.direccion
        bloques = self.padre.paredes + self.padre.rocas + \
            self.padre.fuegos + self.padre.estrella
        pos_fantasmas = []
        for id in self.padre.entidades.keys():
            if id != self.id:
                fantasma = self.padre.entidades[id]
                pos_fantasmas.append((fantasma.x, fantasma.y))
        tope_rocas = checkear_tope_roca(
            x, y, direccion, self.padre.rocas, bloques + pos_fantasmas)
        tope_muros = checkear_tope(x, y, direccion, self.padre.paredes)
        if tope_muros is True or tope_rocas is True:
            self.timer_movimiento.stop()
            self.padre.luigi_caminando = False
        else:
            if tope_rocas is False:
                viejo_x, viejo_y = nueva_posicion(x, y, direccion)
                self.padre.rocas.remove((viejo_x, viejo_y))
                nuevo_x, nuevo_y = nueva_posicion(viejo_x, viejo_y, direccion)
                self.padre.rocas.append((nuevo_x, nuevo_y))
                self.padre.senal_mover_roca.emit(viejo_x // p.PIXELES_CASILLA,
                                                 viejo_y // p.PIXELES_CASILLA,
                                                 nuevo_x // p.PIXELES_CASILLA,
                                                 nuevo_y // p.PIXELES_CASILLA)
            self.mover()
            if (self.x % p.PIXELES_CASILLA,
                    self.y % p.PIXELES_CASILLA) == (0, 0):
                self.timer_movimiento.stop()
                self.padre.luigi_caminando = False
                for id in self.padre.entidades.keys():
                    entidad = self.padre.entidades[id]
                    if (entidad.x, entidad.y) == (self.x, self.y) \
                            and id != self.id:
                        self.padre.vida -= 1

    def morir(self):
        self.padre.entidades.pop(self.id)
        self.padre.senal_eliminar_entidad.emit(self.id)
        del self


class Fantasma(Entidad):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer_movimiento = QTimer(self)
        ponderador_velocidad_fantasmas = random.uniform(
            p.MIN_VELOCIDAD, p.MAX_VELOCIDAD)
        tiempo_movimiento_fantasmas = 1/ponderador_velocidad_fantasmas
        tiempo_por_pixel = p.PIXELES_MOVER/p.PIXELES_CASILLA
        tiempo_por_pixel *= tiempo_movimiento_fantasmas

        self.timer_movimiento.setInterval(int(tiempo_por_pixel))
        self.timer_movimiento.timeout.connect(self.mover)

    def mover(self) -> None:
        casilla = p.PIXELES_CASILLA
        if (self.x, self.y) == (self.padre.luigi.x, self.padre.luigi.y):
            if (self.x % casilla, self.y % casilla) == (0, 0):
                self.padre.vida -= 1
        if (self.x, self.y) in self.padre.fuegos:
            self.morir()
        elif checkear_tope(self.x, self.y, self.direccion,
                           self.padre.paredes + self.padre.rocas):
            cambio = {p.UP: p.DOWN, p.DOWN: p.UP,
                      p.LEFT: p.RIGHT, p.RIGHT: p.LEFT}
            self.direccion = cambio[self.direccion]
            if checkear_tope(self.x, self.y, self.direccion,
                             self.padre.paredes + self.padre.rocas) is False:
                # Esto es para que el fantasma avance solo si no esta encerrado
                super().mover()
        else:
            super().mover()

    def morir(self):
        self.timer_movimiento.stop()
        self.padre.entidades.pop(self.id)
        self.padre.senal_eliminar_entidad.emit(self.id)
        del self


class FantasmaVertical(Fantasma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direccion = p.UP


class FantasmaHorizontal(Fantasma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direccion = p.RIGHT


class FollowerVillain(FantasmaVertical, FantasmaHorizontal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.luigi = self.padre.luigi

    def mover(self):
        self.luigi = self.padre.luigi
        casilla = p.PIXELES_CASILLA
        pos_luigi = (self.luigi.x//casilla, self.luigi.y//casilla)
        if (self.x % casilla, self.y % casilla) == (0, 0) and \
                (self.x//casilla, self.y//casilla) != pos_luigi:
            nueva_casilla = self.bfs()
            if nueva_casilla is not None:
                x, y = nueva_casilla[1][0] * \
                    casilla,  nueva_casilla[1][1]*casilla
                if x - self.x > 0:
                    self.direccion = p.RIGHT
                if x - self.x < 0:
                    self.direccion = p.LEFT
                if y - self.y > 0:
                    self.direccion = p.DOWN
                if y - self.y < 0:
                    self.direccion = p.UP
        super().mover()

    def bfs(self):
        actual = tuple([self.x//p.PIXELES_CASILLA, self.y//p.PIXELES_CASILLA])
        cola = deque([[actual]])
        visitados = set(actual)
        objetivo = (self.luigi.x // p.PIXELES_CASILLA,
                    self.luigi.y // p.PIXELES_CASILLA)
        while len(cola) > 0:
            camino = cola.popleft()
            x, y = camino[-1]
            if (x, y) == objetivo:
                return camino
            choques = self.padre.paredes + self.padre.rocas
            for x2, y2 in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
                if (x2*p.PIXELES_CASILLA, y2*p.PIXELES_CASILLA) not in\
                        choques and (x2, y2) not in visitados:
                    cola.append(camino+[(x2, y2)])
                    visitados.add(tuple([x2, y2]))
