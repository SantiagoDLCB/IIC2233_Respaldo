from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout
import parametros as p
from frontend.frontend_entidades import (FrontendLuigi, FrontendFantasmaH,
                                         FrontendFantasmaV,
                                         FrontendFollowerVillain)
from frontend.bloques import Bloque, Borde, Pared, Roca, Fuego, Estrella


class Mapa(QWidget):
    senal_recargar_nivel = pyqtSignal()
    senal_drop_objeto = pyqtSignal(str, int, int, bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setGeometry(*p.POSICION_INICIAL, p.ANCHO_GRILLA*p.PIXELES_CASILLA,
                         p.LARGO_GRILLA*p.PIXELES_CASILLA)
        self.setFixedSize(self.size())
        self.entidades = {}
        self.grilla = QGridLayout(self)
        self.grilla.setHorizontalSpacing(p.ESPACIADO_MAPA)
        self.grilla.setVerticalSpacing(p.ESPACIADO_MAPA)
        self.grilla.setContentsMargins(*p.MARGENES_MAPA)
        self.setLayout(self.grilla)

    def dragEnterEvent(self, evento):
        evento.accept()

    def dropEvent(self, evento):
        evento.accept()
        pos = evento.pos()
        widget = evento.source()
        x, y = pos.x(), pos.y()
        objetos = {FrontendLuigi: p.LUIGI, FrontendFantasmaV: p.FANTASMA_V,
                   FrontendFantasmaH: p.FANTASMA_H,
                   FrontendFollowerVillain: p.FOLLOWER,
                   Pared: p.PARED, Roca: p.ROCA,
                   Fuego: p.FUEGO, Estrella: p.ESTRELLA}
        self.senal_drop_objeto.emit(objetos[type(widget)], x, y, True)

    def reiniciar_mapa(self, modo_constructor):
        for i in range(0, p.ANCHO_GRILLA * p.LARGO_GRILLA):
            y = i//p.ANCHO_GRILLA
            x = i % p.ANCHO_GRILLA
            bloque = self.grilla.itemAtPosition(y, x)
            if bloque is not None:
                eliminar = bloque.widget()
                del eliminar
        self.cargar_inmovil()
        if modo_constructor is False:
            self.senal_recargar_nivel.emit()

    def cargar_entidad(self, tipo: str, id: int, x: int, y: int):
        entidades = {p.LUIGI: FrontendLuigi, p.FANTASMA_H: FrontendFantasmaH,
                     p.FANTASMA_V: FrontendFantasmaV,
                     p.FOLLOWER: FrontendFollowerVillain}
        if tipo == 'L':
            self.luigi: FrontendLuigi = entidades[tipo](self, id, x, y)
            self.luigi.raise_()
            self.entidades.update({self.luigi .id: self.luigi})
        elif tipo in entidades.keys():
            entidad = entidades[tipo](self, id, x, y)
            entidad.raise_()
            self.entidades.update({entidad.id: entidad})

    def cargar_bloque(self, tipo: str, x: int, y: int):
        blocks = {p.PARED: Pared, p.ROCA: Roca,
                  p.FUEGO: Fuego, p.ESTRELLA: Estrella}
        block_nuevo = blocks[tipo]()
        self.grilla.addWidget(block_nuevo, y, x)

    def cargar_inmovil(self):
        for i in range(p.ANCHO_GRILLA * p.LARGO_GRILLA):
            y = i//p.ANCHO_GRILLA
            x = i % p.ANCHO_GRILLA
            if x in (0, p.ANCHO_GRILLA-1) or y in (0, p.LARGO_GRILLA-1):
                borde = Borde()
                borde.lower()
                self.grilla.addWidget(borde, y, x)
            else:
                bloque = Bloque()
                bloque.lower()
                self.grilla.addWidget(bloque, y, x)

    def mover_entidad(self, id: int, direccion: str, pixeles: int):
        entidad = self.entidades[id]
        entidad.mover(direccion, pixeles)

    def mover_roca(self, x_viejo, y_viejo, x_nuevo, y_nuevo):
        roca, bloque = Roca(), Bloque()
        self.grilla.addWidget(roca, y_nuevo, x_nuevo)
        self.grilla.addWidget(bloque, y_viejo, x_viejo)
        roca.stackUnder(self.luigi)
        for id in self.entidades.keys():
            self.entidades[id].raise_()

    def eliminar_entidad(self, id: int):
        fantasma = self.entidades.pop(id)
        fantasma.setParent(None)
        del fantasma
