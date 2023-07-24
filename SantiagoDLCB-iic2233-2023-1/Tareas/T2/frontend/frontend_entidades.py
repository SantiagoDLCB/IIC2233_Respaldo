from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QDrag
import os
import parametros as p
from collections import deque


class FrontendEntidad(QWidget):
    def __init__(self, padre, id, x, y, * args, **kwargs):
        super().__init__(parent=padre, *args, **kwargs)
        self.constructor = False
        self.id = id
        self.x = x
        self.y = y
        self.imagen = QLabel(self)
        self.setGeometry(self.x, self.y, p.PIXELES_CASILLA, p.PIXELES_CASILLA)
        self.imagen.setFixedSize(self.size())
        self.imagen.setScaledContents(True)
        self.imagenes = {}
        self.show()

    def mover(self, direccion, pixeles):
        self.direccion = direccion
        if self.direccion == p.UP:
            self.y -= pixeles
        if self.direccion == p.DOWN:
            self.y += pixeles
        if self.direccion == p.LEFT:
            self.x -= pixeles
        if self.direccion == p.RIGHT:
            self.x += pixeles
        self.move(self.x, self.y)
        if (self.x % p.CAMBIO_SPRITE, self.y % p.CAMBIO_SPRITE) == (0, 0):
            nueva_imagen = self.imagenes[self.direccion].popleft()
            self.imagen.setPixmap(nueva_imagen)
            self.imagenes[self.direccion].append(nueva_imagen)

    def mouseMoveEvent(self, evento):
        if evento.buttons() == Qt.LeftButton and self.constructor is True:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)


class FrontendLuigi(FrontendEntidad):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargar_imagenes()
        self.imagen.setPixmap(self.imagenes[p.FRONT])

    def cargar_imagenes(self):
        up = deque(QPixmap(os.path.join(*path)) for path in p.PATHS_LUIGI_UP)
        down = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_LUIGI_DOWN)
        left = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_LUIGI_LEFT)
        right = deque(QPixmap(os.path.join(*path))
                      for path in p.PATHS_LUIGI_RIGHT)
        front = QPixmap(os.path.join(*p.PATHS_LUIGI_FRONT))
        self.imagenes = {p.UP: up, p.DOWN: down, p.LEFT: left, p.RIGHT: right,
                         p.FRONT: front}

    def mover(self, direccion, pixeles):
        super().mover(direccion, pixeles)
        if (self.x % p.PIXELES_CASILLA, self.y % p.PIXELES_CASILLA) == (0, 0):
            nueva_imagen = self.imagenes[p.FRONT]
            self.imagen.setPixmap(nueva_imagen)


class FrontendFantasma(FrontendEntidad):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FrontendFantasmaV(FrontendFantasma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        up = deque(QPixmap(os.path.join(*path))
                   for path in p.PATHS_FANTASMA_VERTICAL)
        down = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_FANTASMA_VERTICAL)
        self.imagenes = {p.UP: up, p.DOWN: down}
        self.imagen.setPixmap(self.imagenes[p.UP][0])


class FrontendFantasmaH(FrontendFantasma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargar_imagenes()
        self.imagen.setPixmap(QPixmap(self.imagenes[p.RIGHT][0]))

    def cargar_imagenes(self):
        left = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_FANTASMA_LEFT)
        right = deque(QPixmap(os.path.join(*path))
                      for path in p.PATHS_FANTASMA_RIGHT)
        self.imagenes = {p.LEFT: left, p.RIGHT: right}


class FrontendFollowerVillain(FrontendFantasma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargar_imagenes()
        self.imagen.setPixmap(QPixmap(self.imagenes[p.RIGHT][0]))
        if self.id == p.ID_ENTIDADES_FILTRO:
            self.alternar = QTimer()
            self.alternar.setInterval(1000)
            self.alternar.timeout.connect(self.alternar_sprites)
            self.actual = 0
            self.alternar.start()

    def cargar_imagenes(self):
        up = deque(QPixmap(os.path.join(*path))
                   for path in p.PATHS_FANTASMA_VERTICAL)
        down = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_FANTASMA_VERTICAL)
        left = deque(QPixmap(os.path.join(*path))
                     for path in p.PATHS_FANTASMA_LEFT)
        right = deque(QPixmap(os.path.join(*path))
                      for path in p.PATHS_FANTASMA_RIGHT)
        self.imagenes = {p.UP: up, p.DOWN: down,
                         p.LEFT: left, p.RIGHT: right}

    def alternar_sprites(self):
        if self.actual == 0:
            self.actual = 1
            self.imagen.setPixmap(self.imagenes[p.UP][1])
        else:
            self.actual = 0
            self.imagen.setPixmap(self.imagenes[p.RIGHT][0])
