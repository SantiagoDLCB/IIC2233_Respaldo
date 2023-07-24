import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal


class VentanitaSuprema(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_gui()

    def init_gui(self):
        layout = QVBoxLayout()

        # Ajustamos la geometría de la ventana y su título
        self.setGeometry(200, 100, 600, 600)
        self.setWindowTitle('Ventana con carteles')

        self.label1 = QLabel('Texto:', self)
        # self.label1.move(10, 15)

        layout.addWidget(self.label1)

        self.label2 = QLabel('Esta etiqueta es variable', self)
        self.label2.move(10, 50)

        layout.addWidget(self.label2)
        # Agregamos cuadros de texto mediante QLineEdit(texto_inicial, padre)
        self.edit = QLineEdit('', self)
        self.edit.setGeometry(45, 15, 100, 20)

        # Imagen
        self.label_imagen = QLabel(self)
        self.label_imagen.setGeometry(50, 100, 100, 100)
        ruta_imagen = os.path.join('img', 'python.jpg')
        pixeles = QPixmap(ruta_imagen)
        self.label_imagen.setPixmap(pixeles)
        self.label_imagen.setScaledContents(True)

        self.show()


if __name__ == '__main__':
    app = QApplication([])  # Creamos ls base de la app: QApplication
    ventana = VentanitaSuprema()  # Construirmos un QWidget que será nuestra ventana
    ventana.show()  # Mostramos la ventna
    sys.exit(app.exec())
