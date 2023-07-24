class Mensaje:
    def __init__(self, operacion=None, datos=None):
        self.operacion = operacion
        self.datos = datos


class Jugador:
    def __init__(self, id, vida, dado1, dado2, bot=False):
        self.id = id
        self.__vida = vida
        self.dado1 = dado1
        self.dado2 = dado2
        self.bot = bot

    @property
    def vida(self):
        return self.__vida


class Status:
    def __init__(self, turno_actual, num_anunciado, turno_anterior, num_turno):
        self.turno_actual = turno_actual
        self.num_anunciado = num_anunciado
        self.turno_anterior = turno_anterior
        self.num_turno = num_turno
