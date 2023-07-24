import json
import os
import sys
from frontend.frontend import Frontend
from backend import Backend
from PyQt5.QtWidgets import QApplication


with open(os.path.join('parametros.json')) as parametros:
    PARAMETROS = json.load(parametros)


class Cliente:
    def __init__(self, port, host) -> None:
        self.frontend = Frontend()
        self.backend = Backend(port, host)
        self.conectar_backend_frontend()
        self.conectar_frontend_backend()
        self.backend.conectar_servidor()

    def conectar_backend_frontend(self):
        self.backend.senal_servidor_desconectado.connect(
            self.frontend.servidor_desconectado)
        self.backend.senal_actualizar_cola.connect(
            self.frontend.actualizar_cola)
        self.backend.senal_esconder_cola.connect(
            self.frontend.esconder_cola)
        self.backend.senal_actualizar_jugadores.connect(
            self.frontend.ventana_inicio.actualizar_jugadores)
        self.backend.senal_cambiar_ventana.connect(
            self.frontend.cambiar_ventana)
        self.backend.senal_actualizar_juego.connect(
            self.frontend.ventana_juego.actualizar_juego)
        self.backend.senal_error_juego.connect(
            self.frontend.ventana_juego.error)
        self.backend.senal_perder.connect(self.frontend.ventana_juego.perder)
        self.backend.senal_ganar.connect(self.frontend.ventana_juego.ganar)
        self.backend.senal_actualizar_tiempo.connect(
            self.frontend.ventana_juego.actualizar_tiempo)

    def conectar_frontend_backend(self):
        self.frontend.ventana_inicio.senal_comenzar_juego.connect(
            self.backend.enviar_comenzar_juego)
        self.frontend.ventana_juego.senal_anunciar_valor.connect(
            self.backend.anunciar_valor)
        self.frontend.ventana_juego.senal_pasar_turno.connect(
            self.backend.pasar_turno)
        self.frontend.ventana_juego.senal_cambiar_dados.connect(
            self.backend.cambiar_dados)
        self.frontend.ventana_juego.senal_usar_poder.connect(
            self.backend.usar_poder)
        self.frontend.ventana_juego.senal_dudar.connect(
            self.backend.dudar)
        self.frontend.ventana_juego.senal_see.connect(self.backend.see)


def hook(type_error, traceback):
    print(type_error)
    print(traceback)


sys.__excepthook__ = hook
app = QApplication(sys.argv)
try:
    port = int(sys.argv[1])
except Exception:
    print(PARAMETROS["ERROR_INGRESAR_PUERTO"])
    exit()
client = Cliente(port, PARAMETROS["HOST"])
sys.exit(app.exec())
# if __name__ == '__main__':
#   pass
