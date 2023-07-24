import sys
from PyQt5.QtWidgets import QApplication
from frontend.frontend import VentanaInicio, VentanaJuego
from backend.backend import Logica


class Juego():
    def __init__(self) -> None:
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        self.logica = Logica()

    def iniciar_juego(self):
        self.ventana_juego.panel_lateral.gui_modo_juego()
        self.ventana_inicio.hide()
        self.ventana_juego.show()

    def modo_constructor(self):
        self.ventana_inicio.hide()
        self.ventana_juego.panel_lateral.gui_modo_constructor()
        self.logica.limpiar_constructor()
        self.ventana_juego.show()

    def cambio_modo(self):
        self.ventana_juego.panel_lateral.gui_modo_juego()
        self.logica.reiniciar_nivel()
        self.logica.timer_temporizador.start()

    def conectar(self):
        self.ventana_inicio.senal_intentar_login.connect(
            self.logica.intentar_login)
        self.logica.senal_error_nombre.connect(
            self.ventana_inicio.error_nombre)
        self.logica.senal_iniciar_juego.connect(self.iniciar_juego)
        self.logica.senal_modo_constructor.connect(self.modo_constructor)

        # Modo Constructor
        self.ventana_juego.mapa.senal_drop_objeto.connect(
            self.logica.drop_objeto)
        self.ventana_juego.panel_lateral.senal_drop_objeto.connect(
            self.logica.drop_objeto)
        self.ventana_juego.senal_drop_objeto.connect(
            self.logica.drop_objeto)
        self.logica.senal_error_drop.connect(
            self.ventana_juego.drop_error)
        self.ventana_juego.panel_lateral.senal_limpiar_constructor.connect(
            self.logica.limpiar_constructor)
        self.logica.senal_actualizar_obj_restantes.connect(
            self.ventana_juego.panel_lateral.actualizar_objetos_restantes)
        self.ventana_juego.panel_lateral.senal_jugar_constructor.connect(
            self.cambio_modo)
        # s
        self.ventana_juego.mapa.senal_recargar_nivel.connect(
            self.logica.recargar_nivel)
        self.logica.senal_reiniciar_mapa.connect(
            self.ventana_juego.mapa.reiniciar_mapa)
        ###
        self.logica.senal_actualizar_vidas.connect(
            self.ventana_juego.panel_lateral.actualizar_vidas)
        self.logica.senal_actualizar_temporizador.connect(
            self.ventana_juego.panel_lateral.actualizar_temporizador)

        ####
        self.logica.senal_crear_entidad.connect(
            self.ventana_juego.mapa.cargar_entidad)
        self.logica.senal_crear_bloque.connect(
            self.ventana_juego.mapa.cargar_bloque)
        ##
        self.ventana_juego.senal_tecla.connect(self.logica.tecla)
        ##
        self.ventana_juego.panel_lateral.senal_pausa.connect(self.logica.pausa)
        self.ventana_juego.senal_cheatcode_kil.connect(
            self.logica.cheatcode_kil)
        self.ventana_juego.senal_cheatcode_inf.connect(
            self.logica.cheatcode_inf)

        ##
        self.ventana_juego.senal_capturar_estrella.connect(
            self.logica.capturar_estrella)
        self.logica.senal_mover_entidad.connect(
            self.ventana_juego.mapa.mover_entidad)
        self.logica.senal_mover_roca.connect(
            self.ventana_juego.mapa.mover_roca)
        self.logica.senal_eliminar_entidad.connect(
            self.ventana_juego.mapa.eliminar_entidad)
        self.logica.senal_perder.connect(self.ventana_juego.perder)
        self.logica.senal_ganar.connect(self.ventana_juego.ganar)

        ##
        self.ventana_juego.senal_volver_jugar.connect(self.logica.volver_jugar)


def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == '__main__':
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    juego = Juego()
    juego.conectar()
    sys.exit(app.exec())
