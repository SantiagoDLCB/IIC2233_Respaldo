import socket
from constantes import SIZE_BUFFER
from PyQt5.QtCore import QObject, pyqtSignal


class Logica(QObject):

    senal_update_label = pyqtSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.socket_cliente.connect((self.host, self.port))

    def mandar_comando(self, comando: str) -> None:
        self.socket_cliente.send(comando.encode("utf-8"))
        data = self.socket_cliente.recv(SIZE_BUFFER).decode('utf-8')
        self.senal_update_label.emit(data)