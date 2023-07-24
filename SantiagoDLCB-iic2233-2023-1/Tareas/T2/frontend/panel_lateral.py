
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QComboBox, QLabel, QPushButton, QVBoxLayout)
import parametros as p
from frontend.frontend_entidades import (FrontendLuigi, FrontendFantasmaH,
                                         FrontendFantasmaV,
                                         FrontendFollowerVillain)
from frontend.bloques import Pared, Roca, Fuego, Estrella


class PanelLateral(QWidget):

    senal_pausa = pyqtSignal(bool)
    senal_limpiar_constructor = pyqtSignal()
    senal_jugar_constructor = pyqtSignal()
    senal_drop_objeto = pyqtSignal(str, int, int, bool)

    def __init__(self, padre, *args, **kwargs) -> None:
        super().__init__(padre, *args, **kwargs)
        self.setAcceptDrops(True)
        self.padre = padre
        self.layout_panel = QVBoxLayout()
        self.setLayout(self.layout_panel)

    def gui_modo_juego(self):
        while self.layout_panel.count() != 0:
            widget = self.layout_panel.itemAt(0).widget()
            self.layout_panel.removeWidget(widget)
            if widget is not None:
                widget.setParent(None)

        self.etiqueta_tiempo = QLabel(
            p.TEXTO_ETIQUETA_TIEMPO + str(p.TIEMPO_CUENTA_REGRESIVA), self)
        self.etiqueta_vidas = QLabel(
            p.TEXTO_ETIQUETA_VIDAS + str(p.CANTIDAD_VIDAS), self)
        self.boton_pausa = QPushButton(p.TEXTO_BOTON_PAUSA_FALSE, self)
        self.boton_pausa.setCheckable(True)
        self.boton_pausa.clicked.connect(self.pausar)
        self.layout_panel.addWidget(self.etiqueta_tiempo)
        self.layout_panel.addWidget(self.etiqueta_vidas)
        self.layout_panel.addWidget(self.boton_pausa)
        self.layout_panel.addStretch()

    def gui_modo_constructor(self):
        self.dict_objetos_restantes = {}
        # Objetos Restantes

        self.objetos_restantes = QLabel()

        # opciones segun filtro
        self.opciones = OpcionesConstructor(self)

        # filtro
        self.filtro = QComboBox()
        self.filtro.addItems([p.TEXTO_FILTRO_TODOS, p.TEXTO_FILTRO_BLOQUES,
                              p.TEXTO_FILTRO_ENTIDADES])
        self.opciones.elegir_grupo()
        self.filtro.currentTextChanged.connect(
            self.opciones.elegir_grupo)

        # Botones Limpiar Jugar
        self.boton_limpiar = QPushButton()
        self.boton_limpiar.setText(p.TEXTO_BOTON_LIMPIAR)
        self.boton_limpiar.clicked.connect(self.senal_limpiar_constructor.emit)

        self.boton_jugar = QPushButton()
        self.boton_jugar.setText(p.TEXTO_BOTON_JUGAR)
        self.boton_jugar.clicked.connect(self.jugar)

        # layouts
        self.layout_panel.addWidget(self.filtro)
        self.layout_panel.addWidget(self.opciones)
        self.layout_panel.addStretch()
        self.layout_panel.addWidget(self.objetos_restantes)
        self.layout_panel.addWidget(self.boton_limpiar)
        self.layout_panel.addWidget(self.boton_jugar)

    def actualizar_vidas(self, vida):
        self.etiqueta_vidas.setText(f"Vidas: {vida}")

    def actualizar_temporizador(self, tiempo):
        self.etiqueta_tiempo.setText(p.TEXTO_ETIQUETA_TIEMPO + str(tiempo))

    def actualizar_objetos_restantes(self, obj_restantes: dict):
        self.dict_objetos_restantes = obj_restantes
        t = ''
        for objeto in self.dict_objetos_restantes.keys():
            t += f'{objeto}:  {obj_restantes[objeto]}\n'
        self.objetos_restantes.setText(t)

    def pausar(self):
        if self.boton_pausa.isChecked():
            self.senal_pausa.emit(True)
            self.boton_pausa.setText(p.TEXTO_BOTON_PAUSA_TRUE)
        else:
            self.boton_pausa.setText(p.TEXTO_BOTON_PAUSA_FALSE)
            self.senal_pausa.emit(False)

    def jugar(self):
        luigi_restante = self.dict_objetos_restantes[p.LUIGI]
        estrella_restante = self.dict_objetos_restantes[p.ESTRELLA]
        if luigi_restante == 0 and estrella_restante == 0:
            self.senal_jugar_constructor.emit()

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
                   Pared: p.PARED, Roca: p.ROCA, Fuego: p.FUEGO,
                   Estrella: p.ESTRELLA}
        self.senal_drop_objeto.emit(objetos[type(widget)], x, y, False)


class OpcionesConstructor(QWidget):
    def __init__(self, padre, *args, **kwargs) -> None:
        super().__init__(padre, *args, **kwargs)
        self.padre = padre
        self.layout_opciones = QVBoxLayout()
        self.setLayout(self.layout_opciones)
        id = p.ID_ENTIDADES_FILTRO
        self.luigi = FrontendLuigi(self, id, *p.POSICION_INICIAL)
        self.fantasmaV = FrontendFantasmaV(self, id, *p.POSICION_INICIAL)
        self.fantasmaH = FrontendFantasmaH(self, id, *p.POSICION_INICIAL)
        self.followervillain = FrontendFollowerVillain(
            self, id, *p.POSICION_INICIAL)
        self.pared = Pared(self)
        self.roca = Roca(self)
        self.fuego = Fuego(self)
        self.estrella = Estrella(self)
        self.bloques = [self.pared, self.roca, self.fuego, self.estrella]
        self.entidades = [self.luigi, self.fantasmaV,
                          self.fantasmaH, self.followervillain]
        self.todos = self.entidades + self.bloques
        for objeto in self.todos:
            objeto.constructor = True
            objeto.setFixedSize(p.PIXELES_CASILLA, p.PIXELES_CASILLA)
            objeto.imagen.setStyleSheet(p.STYLE_SHEET_OBJETOS_PANEL)

    def dragEnterEvent(self, evento):
        evento.accept()

    def elegir_grupo(self):
        grupos = {p.TEXTO_FILTRO_TODOS: self.todos,
                  p.TEXTO_FILTRO_BLOQUES: self.bloques,
                  p.TEXTO_FILTRO_ENTIDADES: self.entidades}
        self.eliminar_todos()
        for elemento in grupos[self.padre.filtro.currentText()]:
            elemento.setParent(self)
            self.layout_opciones.addWidget(elemento)

    def eliminar_todos(self):
        while self.layout_opciones.count() != 0:
            widget = self.layout_opciones.itemAt(0).widget()
            self.layout_opciones.removeWidget(widget)
            widget.setParent(None)
