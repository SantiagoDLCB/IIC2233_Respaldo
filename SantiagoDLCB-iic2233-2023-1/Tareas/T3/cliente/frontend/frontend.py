from collections import deque
import json
import os
import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap

from frontend.icono_jugador import IconoJugador


with open(os.path.join('parametros.json')) as parametros:
    PARAMETROS = json.load(parametros)


class Frontend():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        self.mensaje_cola = QMessageBox()

    def cambiar_ventana(self, datos):
        self.ventana_inicio.hide()
        self.ventana_juego.actualizar_juego(datos)
        self.ventana_juego.show()

    def servidor_desconectado(self):
        self.mensaje_servidor = QMessageBox()
        self.mensaje_servidor.setText(PARAMETROS["TEXTO_DESCONECTADO"])
        self.boton_salir = self.mensaje_servidor.addButton(
            PARAMETROS["TEXTO_SALIR"], QMessageBox.YesRole)
        self.boton_salir.clicked.connect(sys.exit)
        self.mensaje_servidor.rejected.connect(sys.exit)
        self.mensaje_servidor.exec_()

    def actualizar_cola(self, jugando):
        self.mensaje_cola.close()
        self.mensaje_cola = QMessageBox()
        self.boton_OK = self.mensaje_cola.addButton(
            PARAMETROS["TEXTO_SALIR"], QMessageBox.YesRole)
        self.boton_OK.clicked.connect(sys.exit)
        if jugando:
            self.mensaje_cola.setText(PARAMETROS["TEXTO_PARTIDA_ACTIVA"])
        else:
            self.mensaje_cola.setText(PARAMETROS["TEXTO_COLA_LLENA"])
        self.mensaje_cola.exec_()

    def esconder_cola(self):
        self.mensaje_cola.close()


class VentanaInicio(QWidget):
    senal_comenzar_juego = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(*PARAMETROS["GEOMETRIA_INICIO"])
        self.setFixedSize(self.size())
        self.crear_fondo()
        self.crear_layout_principal()
        self.show()

    def crear_fondo(self):
        self.background = QLabel(self)
        self.background.setPixmap(
            QPixmap(os.path.join(*PARAMETROS["PATH_FONDO_INICIO"])))
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.setFixedSize(self.background.size())
        # Transparente a eventos del mouse
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)

    def crear_layout_principal(self):
        self.titulo_espera = QLabel(PARAMETROS["TEXTO_TITULO_ESPERA"])
        self.titulo_espera.setStyleSheet(
            "".join(PARAMETROS["STYLE_TITULO_ESPERA"]))
        self.grilla_principal = QHBoxLayout()
        self.boton_comenzar = QPushButton(PARAMETROS["TEXTO_COMENZAR"])
        self.boton_comenzar.clicked.connect(self.senal_comenzar_juego.emit)
        self.boton_salir = QPushButton(PARAMETROS["TEXTO_SALIR"])
        self.boton_salir.clicked.connect(exit)
        self.layout_principal = QVBoxLayout()
        self.layout_principal.addSpacing(PARAMETROS["ESPACIADO_TITULO"])
        self.layout_principal.addWidget(self.titulo_espera)
        self.layout_principal.addStretch()
        self.layout_principal.addLayout(self.grilla_principal)
        self.layout_principal.addStretch()
        self.layout_principal.addWidget(self.boton_comenzar)
        self.layout_principal.addWidget(self.boton_salir)
        self.setLayout(self.layout_principal)

    def actualizar_jugadores(self, lista_id_jugadores: list):
        while self.grilla_principal.count() != 0:
            widget = self.grilla_principal.itemAt(0).widget()
            self.grilla_principal.removeWidget(widget)
            widget.setParent(None)
            del widget
        for jugador in lista_id_jugadores:
            self.grilla_principal.addWidget(
                IconoJugador(jugador, modo_juego=False))


class VentanaJuego(QWidget):
    senal_anunciar_valor = pyqtSignal(str)
    senal_pasar_turno = pyqtSignal()
    senal_cambiar_dados = pyqtSignal()
    senal_usar_poder = pyqtSignal(str)
    senal_dudar = pyqtSignal()
    senal_see = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(*PARAMETROS["GEOMETRIA_JUEGO"])
        self.setFixedSize(self.size())
        self.crear_fondo()
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(*PARAMETROS["MARGENES_JUEGO"])
        self.setLayout(self.layout_principal)
        self.historial = deque(PARAMETROS["HISTORIAL_INICIO"])
        self.tiempo = QLabel()
        self.tiempo.setStyleSheet("".join(PARAMETROS["STYLE_TIEMPO"]))
        self.cargar_panel_superior()
        self.cargar_grilla()

    def crear_fondo(self):
        self.background = QLabel(self)
        self.background.setPixmap(
            QPixmap(os.path.join(*PARAMETROS["PATH_FONDO_JUEGO"])))
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.setFixedSize(self.background.size())
        # Transparente a eventos del mouse
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)

    def cargar_panel_superior(self):
        self.turno_actual = QLabel()
        self.layout_datos = QHBoxLayout()
        self.numero_mayor = QLabel()
        self.turno_anterior = QLabel()
        self.numero_turno = QLabel()
        for label in [self.turno_actual, self.numero_mayor,
                      self.turno_anterior, self.numero_turno]:
            label.setStyleSheet("".join(PARAMETROS["STYLE_STATUS"]))
        self.layout_principal.addWidget(self.turno_actual)
        self.layout_principal.addSpacing(
            PARAMETROS["ESPACIADO_PANEL_SUPERIOR"])
        self.layout_principal.addLayout(self.layout_datos)
        self.layout_datos.addWidget(self.numero_mayor)
        self.layout_datos.addWidget(self.turno_anterior)
        self.layout_datos.addWidget(self.numero_turno)

    def cargar_grilla(self):
        self.grilla_principal = QGridLayout()
        for n in range(PARAMETROS["DIMENSION_GRILLA"]):
            p = PARAMETROS["PIXELES_GRILLA"]
            self.grilla_principal.setColumnMinimumWidth(n, p)
            self.grilla_principal.setRowMinimumHeight(n, p)
        self.layout_principal.addStretch()
        self.layout_principal.addLayout(self.grilla_principal)
        self.grilla_principal.addWidget(self.tiempo, *PARAMETROS["POS_TIEMPO"])
        self.cargar_panel_acciones()
        self.grilla_principal.addLayout(
            self.grilla_acciones, *PARAMETROS["POS_ACCIONES"])
        self.layout_principal.addStretch()

    def cargar_jugadores(self, dict_jugadores: dict):
        c = 0
        for jug in dict_jugadores:
            jugador = IconoJugador(jug.id, jug.vida, jug.dado1, jug.dado2)
            posiciones = [PARAMETROS["POS_JUG_1"], PARAMETROS["POS_JUG_2"],
                          PARAMETROS["POS_JUG_3"], PARAMETROS["POS_JUG_4"]]
            self.grilla_principal.addWidget(jugador, *posiciones[c])
            c += 1

    def cargar_panel_acciones(self):
        self.grilla_acciones = QGridLayout()
        self.boton_anunciar_valor = QPushButton(PARAMETROS["ANUNCIAR_VALOR"])
        self.boton_anunciar_valor.setFixedWidth(PARAMETROS["ANCHO_ACCIONES"])
        self.cuadro_texto = QLineEdit()
        self.cuadro_texto.setPlaceholderText('Ingrese valor aqui')
        self.boton_anunciar_valor.clicked.connect(self.anunciar_valor)
        self.cuadro_texto.setFixedWidth(PARAMETROS["ANCHO_ACCIONES"])
        self.boton_pasar_turno = QPushButton(PARAMETROS["PASAR_TURNO"])
        self.boton_pasar_turno.clicked.connect(self.senal_pasar_turno.emit)
        self.boton_cambiar_dados = QPushButton(PARAMETROS["CAMBIAR_DADOS"])
        self.boton_cambiar_dados.clicked.connect(self.senal_cambiar_dados.emit)
        self.boton_usar_poder = QPushButton(PARAMETROS["USAR_PODER"])
        self.boton_usar_poder.clicked.connect(self.usar_poder)
        self.boton_dudar = QPushButton(PARAMETROS["DUDAR"])
        self.boton_dudar.clicked.connect(self.senal_dudar.emit)
        self.acciones = [self.boton_anunciar_valor, self.cuadro_texto,
                         self.boton_pasar_turno, self.boton_cambiar_dados,
                         self.boton_usar_poder, self.boton_dudar]
        for pos in range(len(self.acciones)):
            self.grilla_acciones.addWidget(self.acciones[pos], pos//2, pos % 2)

    def anunciar_valor(self):
        valor = self.cuadro_texto.text()
        self.senal_anunciar_valor.emit(valor)

    def usar_poder(self):
        objetivo = self.cuadro_texto.text()
        self.senal_usar_poder.emit(objetivo)

    def actualizar_juego(self, datos: list):
        status_juego = datos[0]
        self.turno_actual.setText(f'Turno de {status_juego.turno_actual}')
        self.numero_mayor.setText(
            f'Numero mayor anunciado: {status_juego.num_anunciado}')
        self.turno_anterior.setText(
            f'Turno anterior fue: {status_juego.turno_anterior}')
        self.numero_turno.setText(
            f'Numero Turno: {status_juego.num_turno}')
        self.eliminar_jugadores()
        self.cargar_jugadores(datos[1])

    def eliminar_jugadores(self):
        for posicion in [PARAMETROS["POS_JUG_1"], PARAMETROS["POS_JUG_2"],
                         PARAMETROS["POS_JUG_3"], PARAMETROS["POS_JUG_4"]]:
            widget = self.grilla_principal.itemAtPosition(*posicion)
            if widget is not None:
                widget = widget.widget()
                self.grilla_principal.removeWidget(widget)
                widget.setParent(None)

    def error(self, mensaje: str):
        error = QMessageBox()
        error.setText(mensaje)
        error.exec_()

    def perder(self):
        self.layout_mensaje_final = QVBoxLayout()
        for accion in self.acciones:
            accion.setParent(None)
        self.eliminar_jugadores()
        self.grilla_principal.removeItem(self.grilla_acciones.layout())
        self.grilla_acciones.setParent(None)
        self.etiqueta_perder = QLabel(PARAMETROS["TEXTO_PERDISTE"])
        self.etiqueta_perder.setStyleSheet(
            "".join(PARAMETROS["STYLE_RESULTADO"]))
        self.layout_mensaje_final.addWidget(self.etiqueta_perder)
        self.etiqueta_cerrar = QLabel(PARAMETROS["TEXTO_CERRAR"])
        self.etiqueta_cerrar.setStyleSheet("".join(PARAMETROS["STYLE_TIEMPO"]))
        self.layout_mensaje_final.addWidget(self.etiqueta_cerrar)
        self.tiempo.setParent(None)
        for n in range(PARAMETROS["DIMENSION_GRILLA"]):
            self.grilla_principal.setColumnMinimumWidth(n, 0)
        self.grilla_principal.addLayout(
            self.layout_mensaje_final, *PARAMETROS["POS_TIEMPO"])

    def ganar(self):
        self.layout_mensaje_final = QVBoxLayout()
        for accion in self.acciones:
            accion.setParent(None)
        self.eliminar_jugadores()
        self.etiqueta_ganar = QLabel(PARAMETROS["TEXTO_GANASTE"])
        self.etiqueta_ganar.setStyleSheet(
            "".join(PARAMETROS["STYLE_RESULTADO"]))
        self.layout_mensaje_final.addWidget(self.etiqueta_ganar)
        self.etiqueta_cerrar = QLabel(PARAMETROS["TEXTO_CERRAR"])
        self.etiqueta_cerrar.setStyleSheet("".join(PARAMETROS["STYLE_TIEMPO"]))
        self.layout_mensaje_final.addWidget(self.etiqueta_cerrar)
        self.tiempo.setParent(None)
        for n in range(PARAMETROS["DIMENSION_GRILLA"]):
            self.grilla_principal.setColumnMinimumWidth(n, 0)
        self.grilla_principal.addLayout(
            self.layout_mensaje_final, *PARAMETROS["POS_TIEMPO"])

    def actualizar_tiempo(self, t):
        self.tiempo.setText(PARAMETROS["TEXTO_TIEMPO"]+str(t))

    def keyPressEvent(self, event):
        self.historial.popleft()
        if event.key() == Qt.Key_S:
            self.historial.append(PARAMETROS["LETRA_S"])
        elif event.key() == Qt.Key_E:
            self.historial.append(PARAMETROS["LETRA_E"])
        else:
            self.historial.append(None)
        if self.historial == deque(PARAMETROS["SECUENCIA_SEE"]):
            self.senal_see.emit()
