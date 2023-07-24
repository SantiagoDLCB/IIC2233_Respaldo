import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap

with open(os.path.join('parametros.json')) as parametros:
    PARAMETROS = json.load(parametros)


class IconoJugador(QWidget):
    def __init__(self, nombre, vidas=0, dado1=1, dado2=1, modo_juego=True,
                 * args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.modo_juego = modo_juego
        self.icono = QLabel()
        self.icono.setPixmap(QPixmap(os.path.join(*PARAMETROS["PATH_ICONO"])))
        self.icono.setScaledContents(True)
        self.icono.setFixedWidth(PARAMETROS["DIMENSION_ICONO"])
        self.icono.setFixedHeight(PARAMETROS["DIMENSION_ICONO"])
        self.etiqueta_id = QLabel(self.nombre)
        self.etiqueta_id.setStyleSheet("".join(PARAMETROS["STYLE_ID"]))
        self.layout_horizontal = QHBoxLayout()
        self.layout_vertical = QVBoxLayout()
        self.layout_vertical.addWidget(self.icono, alignment=Qt.AlignCenter)
        self.layout_vertical.addWidget(self.etiqueta_id)
        self.layout_horizontal.addStretch()
        self.layout_horizontal.addLayout(self.layout_vertical)
        self.layout_dados = QVBoxLayout()
        self.layout_horizontal.addLayout(self.layout_dados)
        self.layout_horizontal.addStretch()
        self.setLayout(self.layout_horizontal)
        if modo_juego:
            self.cargar_modo_juego(vidas, dado1, dado2)

    def cargar_modo_juego(self, vidas, dado1, dado2):
        self.vidas = QLabel(PARAMETROS["TEXTO_VIDAS"]+str(vidas))
        self.vidas.setStyleSheet("".join(PARAMETROS["STYLE_VIDAS"]))
        self.layout_vertical.addWidget(self.vidas)
        self.crear_dados()
        self.actualizar_dados(dado1, dado2)

    def crear_dados(self):
        paths_dados = [PARAMETROS["PATH_DICE_HIDE"],
                       PARAMETROS["PATH_DICE_1"],
                       PARAMETROS["PATH_DICE_2"],
                       PARAMETROS["PATH_DICE_3"],
                       PARAMETROS["PATH_DICE_4"],
                       PARAMETROS["PATH_DICE_5"],
                       PARAMETROS["PATH_DICE_6"]]
        self.imgs_dados = [QPixmap(os.path.join(*path1))
                           for path1 in paths_dados]
        self.dado1 = QLabel()
        self.dado1.setFixedSize(PARAMETROS["DIMENSION_DADO"],
                                PARAMETROS["DIMENSION_DADO"])
        self.dado2 = QLabel()
        self.dado2.setFixedSize(PARAMETROS["DIMENSION_DADO"],
                                PARAMETROS["DIMENSION_DADO"])
        self.layout_dados.addStretch()
        self.layout_dados.addWidget(self.dado1)
        self.layout_dados.addWidget(self.dado2)
        self.layout_dados.addStretch()

    def actualizar_dados(self, dado1, dado2):
        self.dado1.setParent(self)
        self.dado1.setPixmap(self.imgs_dados[dado1])
        self.dado1.setScaledContents(True)
        self.dado2.setParent(self)
        self.dado2.setPixmap(self.imgs_dados[dado2])
        self.dado2.setScaledContents(True)
