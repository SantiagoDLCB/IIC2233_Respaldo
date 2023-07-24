
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPixmap, QDrag
import parametros as p
import os


class Bloque(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructor = False
        self.imagen = QLabel(self)
        self.imagen.setFixedSize(p.PIXELES_CASILLA, p.PIXELES_CASILLA)
        self.imagen.setScaledContents(True)
        self.imagen.setStyleSheet(p.STYLE_SHEET_BLOQUES_JUEGO)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and self.constructor is True:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)


class Borde(Bloque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagen.setPixmap(QPixmap(os.path.join(*p.PATH_BORDE)))


class Pared(Bloque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagen.setPixmap(QPixmap(os.path.join(*p.PATH_PARED)))


class Roca(Bloque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagen.setPixmap(QPixmap(os.path.join(*p.PATH_ROCA)))


class Fuego(Bloque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagen.setPixmap(QPixmap(os.path.join(*p.PATH_FUEGO)))


class Estrella(Bloque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagen.setPixmap(QPixmap(os.path.join(*p.PATH_ESTRELLA)))
