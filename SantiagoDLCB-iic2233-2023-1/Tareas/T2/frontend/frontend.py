from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QComboBox, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSound
import parametros as p
import os
from frontend.frontend_entidades import (FrontendLuigi, FrontendFantasmaH,
                                         FrontendFantasmaV,
                                         FrontendFollowerVillain)
from frontend.bloques import Pared, Roca, Fuego, Estrella
from frontend.mapa import Mapa
from frontend.panel_lateral import PanelLateral


class VentanaInicio(QWidget):
    senal_intentar_login = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle(p.TITULO_VENTANA_INICIO)
        self.setGeometry(*p.POSICION_VENTANA_INICIO, *p.TAMANO_VENTANA_INICIO)
        self.setFixedSize(self.size())
        self.crear_background()
        self.crear_logo()
        self.crear_lista_mapas()
        self.crear_etiqueta()
        self.crear_cuadro_texto()
        self.crear_boton_login()
        self.crear_boton_salir()
        self.crear_layouts()
        self.show()

    def crear_background(self):
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(os.path.join(*p.PATH_BACKGROUND)))
        self.background.setScaledContents(True)
        self.background.setGeometry(
            *p.POSICION_INICIAL, *p.TAMANO_VENTANA_INICIO)
        self.background.setFixedSize(self.background.size())
        # Transparente a eventos del mouse
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)

    def crear_logo(self):
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(os.path.join(*p.PATH_LOGO)))
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(*p.TAMANO_LOGO)
        self.logo.move(*p.POSICION_INICIAL)

    def crear_lista_mapas(self):
        self.lista_mapas = QComboBox()
        lista_mapas = [p.MODO_CONSTRUCTOR] + os.listdir(*p.PATH_CARPETA_MAPAS)
        self.lista_mapas.addItems(lista_mapas)

    def crear_etiqueta(self):
        self.etiqueta = QLabel(p.TEXTO_ETIQUETA_NOMBRE)
        self.etiqueta.setGeometry(
            *p.POSICION_INICIAL, *p.TAMANO_ETIQUETA_NOMBRE)
        self.etiqueta.setStyleSheet(p.STYLE_SHEET_ETIQUETA_NOMBRE)

    def crear_cuadro_texto(self):
        self.usuario = QLineEdit(self)
        self.usuario.setGeometry(*p.POSICION_INICIAL, *p.TAMANO_CUADRO_TEXTO)

    def crear_boton_login(self):
        self.login = QPushButton(p.TEXTO_BOTON_LOGIN)
        self.login.setGeometry(*p.POSICION_INICIAL, *p.TAMANO_BOTON_LOGIN)
        self.login.clicked.connect(self.obtener_nombre)

    def crear_boton_salir(self):
        self.salir_inicio = QPushButton(p.TEXTO_BOTON_SALIR_INICIO)
        self.salir_inicio.setGeometry(*p.POSICION_INICIAL, *
                                      p.TAMANO_BOTON_SALIR_INICIO)
        self.salir_inicio.clicked.connect(exit)

    def crear_layouts(self):
        layout_logo = QHBoxLayout()
        layout_logo.addWidget(self.logo)
        layout_usuario = QHBoxLayout()
        layout_usuario.addWidget(self.etiqueta)
        layout_usuario.addWidget(self.usuario)
        layout_usuario.addWidget(self.login)
        layout_usuario.addWidget(self.salir_inicio)
        layout = QVBoxLayout()
        layout.addSpacing(p.ESPACIADO_VENTANA_INICIO)
        layout.addLayout(layout_logo)
        layout.addWidget(self.lista_mapas)
        layout.addLayout(layout_usuario)
        layout.addStretch()
        self.setLayout(layout)

    def error_nombre(self, mensaje):
        error = QMessageBox()
        error.setWindowTitle(p.TITULO_POPUP_ERROR_NOMBRE)
        error.setText(mensaje)
        error.exec_()

    def obtener_nombre(self):
        nombre = self.usuario.text()
        mapa_seleccionado = self.lista_mapas.currentText()
        self.senal_intentar_login.emit(nombre, mapa_seleccionado)


class VentanaJuego(QWidget):
    senal_tecla = pyqtSignal(str)
    senal_capturar_estrella = pyqtSignal()
    ultimas_teclas = [False, False, False]
    senal_cheatcode_kil = pyqtSignal()
    senal_cheatcode_inf = pyqtSignal()
    senal_drop_objeto = pyqtSignal(str, int, int, bool)
    senal_volver_jugar = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.vidas = p.CANTIDAD_VIDAS
        self.setWindowTitle(p.TITULO_VENTANA_JUEGO)
        self.setGeometry(*p.POSICION_VENTANA_JUEGO, *p.TAMANO_VENTANA_JUEGO)
        self.setFixedSize(self.size())
        self.mapa: Mapa = Mapa()
        self.layout_paneles = QHBoxLayout()
        self.panel_lateral = PanelLateral(self)
        self.layout_paneles.addWidget(self.panel_lateral)
        self.layout_paneles.addStretch()
        self.layout_paneles.addWidget(self.mapa)
        self.setLayout(self.layout_paneles)

    def keyPressEvent(self, event):
        teclas_cheatcodes = {Qt.Key_K: 'K', Qt.Key_I: 'I',
                             Qt.Key_L: 'L', Qt.Key_N: 'N', Qt.Key_F: 'F'}
        if event.key() in teclas_cheatcodes.keys():
            self.ultimas_teclas = self.ultimas_teclas[1:] + \
                [teclas_cheatcodes[event.key()]]
        else:
            self.ultimas_teclas = self.ultimas_teclas[1:] + [False]
            if event.key() == Qt.Key_G:
                self.senal_capturar_estrella.emit()
            elif event.key() == Qt.Key_P:
                self.panel_lateral.boton_pausa.click()
            elif event.key() == Qt.Key_W:
                self.senal_tecla.emit(p.UP)
            elif event.key() == Qt.Key_A:
                self.senal_tecla.emit(p.LEFT)
            elif event.key() == Qt.Key_S:
                self.senal_tecla.emit(p.DOWN)
            elif event.key() == Qt.Key_D:
                self.senal_tecla.emit(p.RIGHT)
        if self.ultimas_teclas == p.COMBINACION_CHEATCODE1:
            self.senal_cheatcode_kil.emit()
        if self.ultimas_teclas == p.COMBINACION_CHEATCODE2:
            self.senal_cheatcode_inf.emit()

    def dragEnterEvent(self, evento):
        evento.accept()

    def dropEvent(self, evento):
        evento.accept()
        pos = evento.pos()
        widget = evento.source()
        x, y = pos.x(), pos.y()
        objetos = {FrontendLuigi: p.LUIGI, FrontendFantasmaV: p.FANTASMA_V,
                   FrontendFantasmaH: p.FANTASMA_H,
                   FrontendFollowerVillain: p.FOLLOWER, Pared: p.PARED,
                   Roca: p.ROCA, Fuego: p.FUEGO, Estrella: p.ESTRELLA}
        self.senal_drop_objeto.emit(objetos[type(widget)], x, y, False)

    def ganar(self, nombre, puntaje):
        self.hide()
        self.panel_lateral.boton_pausa.click()
        sonido_ganar = QSound(os.path.join(*p.PATH_SONIDO_GANAR))
        sonido_ganar.play()
        ganar = QMessageBox()
        ganar.setWindowTitle(p.TITULO_POPUP_GANAR)
        ganar.setText(nombre + p.MENSAJE_GANAR+str(puntaje))
        self.boton_salir = ganar.addButton(
            p.TEXTO_BOTON_SALIR, QMessageBox.YesRole)
        self.boton_volver = ganar.addButton(
            p.TEXTO_BOTON_VOLVER, QMessageBox.NoRole)
        self.boton_volver.clicked.connect(self.senal_volver_jugar)
        self.boton_volver.clicked.connect(
            self.panel_lateral.boton_pausa.click)
        self.boton_volver.clicked.connect(self.show)
        self.boton_salir.clicked.connect(exit)
        ganar.exec_()

    def perder(self, nombre, razon):
        self.hide()
        self.panel_lateral.boton_pausa.click()
        sonido_perder = QSound(os.path.join(*p.PATH_SONIDO_PERDER))
        sonido_perder.play()
        perder = QMessageBox()
        perder.setWindowTitle(p.TITULO_POPUP_PERDER)
        perder.setText(nombre + razon + p.MENSAJE_PERDER)
        self.boton_salir = perder.addButton(
            p.TEXTO_BOTON_SALIR, QMessageBox.YesRole)
        self.boton_volver = perder.addButton(
            p.TEXTO_BOTON_VOLVER, QMessageBox.NoRole)
        self.boton_volver.clicked.connect(self.senal_volver_jugar.emit)
        self.boton_volver.clicked.connect(
            self.panel_lateral.boton_pausa.click)
        self.boton_volver.clicked.connect(self.show)
        self.boton_salir.clicked.connect(exit)
        perder.exec_()

    def drop_error(self, mensaje: str):
        drop_error = QMessageBox()
        drop_error.setWindowTitle(p.TITULO_POPUP_ERROR_DROP)
        drop_error.setText(mensaje)
        drop_error.exec_()

    def cheatcode_kil(self):
        self.senal_cheatcode_kil.emit()
        for id in self.mapa.entidades.keys():
            if id != self.mapa.luigi.id:
                self.mapa.eliminar_entidad(id)
