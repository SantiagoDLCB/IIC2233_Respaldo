# INICIO
ARENA_INICIAL: str = 'normal'  # 'normal' o 'mojada' o 'rocosa' o 'magnetica'
CANTIDAD_EXCAVADORES_INICIALES: int = 5  # <= cantidad en excavadores.csv


METROS_META: float = 100.0
DIAS_TOTALES_TORNEO: int = 10

POND_ARENA_NORMAL: float = 0.8  # entre 0.1 y 1

# Excavador
PROB_ENCONTRAR_ITEM = 0.3

PROB_ENCONTRAR_TESORO = 0.4  # debe sumar 1 con la siguiente
PROB_ENCONTRAR_CONSUMIBLE = 0.6

# docencio
FELICIDAD_ADICIONAL_DOCENCIO: int = 7
FUERZA_ADICIONAL_DOCENCIO: int = 3
ENERGIA_PERDIDA_DOCENCIO: int = 3

# tareo
ENERGIA_ADICIONAL_TAREO: int = 4
SUERTE_ADICIONAL_TAREO: int = 1
EDAD_ADICIONAL_TAREO: int = 1
FELICIDAD_PERDIDA_TAREO: int = 1

# --------- Evento--------
PROB_INICIAR_EVENTO: int = 0.8

#  Los siguiente parametros deben sumar 1
PROB_LLUVIA: int = 0.4
PROB_TERREMOTO: int = 0.4
PROB_DERRUMBE: int = 0.2
#
METROS_PERDIDOS_DERRUMBE: float = 20.0  # float positivo

FELICIDAD_PERDIDA: int = 2
