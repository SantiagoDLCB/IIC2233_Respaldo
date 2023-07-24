ANCHO_GRILLA = 11  # NO EDITAR
LARGO_GRILLA = 16  # NO EDITAR

# Complete con los demás parámetros
# **********************************************************
# ************ MINIMOS DE ENUNCIADO MODIFICABLE ************
# **********************************************************
MIN_CARACTERES = 4
MAX_CARACTERES = 24
MULTIPLICADOR_PUNTAJE = 3
TIEMPO_CUENTA_REGRESIVA = 125
CANTIDAD_VIDAS = 3
MAX_VELOCIDAD = 0.003
MIN_VELOCIDAD = 0.001
MAXIMO_PARED = 7
MAXIMO_ROCA = 4
MAXIMO_FUEGO = 3
MAXIMO_FANTASMAS_VERTICAL = 4
MAXIMO_FANTASMAS_HORIZONTAL = 4
MAXIMO_FOLLOWER_VILLAIN = 4


# **********************************************************
# ************************ PATHS ***************************
# **********************************************************
# ****VENTANA DE INICIO
PATH_BACKGROUND = ['sprites', 'Fondos', 'fondo_inicio.png']
PATH_LOGO = ['sprites', 'Elementos', 'logo.png']
# ****ENTIDADES
# **LUIGI
PATHS_LUIGI_UP = [('sprites', 'Personajes', 'luigi_up_1.png'),
                  ('sprites', 'Personajes', 'luigi_up_2.png'),
                  ('sprites', 'Personajes', 'luigi_up_3.png')]
PATHS_LUIGI_DOWN = [('sprites', 'Personajes', 'luigi_down_1.png'),
                    ('sprites', 'Personajes', 'luigi_down_2.png'),
                    ('sprites', 'Personajes', 'luigi_down_3.png')]
PATHS_LUIGI_LEFT = [('sprites', 'Personajes', 'luigi_left_1.png'),
                    ('sprites', 'Personajes', 'luigi_left_2.png'),
                    ('sprites', 'Personajes', 'luigi_left_3.png')]
PATHS_LUIGI_RIGHT = [('sprites', 'Personajes', 'luigi_rigth_1.png'),
                     ('sprites', 'Personajes', 'luigi_rigth_2.png'),
                     ('sprites', 'Personajes', 'luigi_rigth_3.png')]
PATHS_LUIGI_FRONT = ['sprites', 'Personajes', 'luigi_front.png']
# **FANTASMAS
PATHS_FANTASMA_VERTICAL = [('sprites', 'Personajes',
                            'red_ghost_vertical_1.png'),
                           ('sprites', 'Personajes',
                            'red_ghost_vertical_2.png'),
                           ('sprites', 'Personajes',
                            'red_ghost_vertical_3.png')]
PATHS_FANTASMA_LEFT = [('sprites', 'Personajes', 'white_ghost_left_1.png'),
                       ('sprites', 'Personajes', 'white_ghost_left_2.png'),
                       ('sprites', 'Personajes', 'white_ghost_left_3.png')]
PATHS_FANTASMA_RIGHT = [('sprites', 'Personajes', 'white_ghost_rigth_1.png'),
                        ('sprites', 'Personajes', 'white_ghost_rigth_2.png'),
                        ('sprites', 'Personajes', 'white_ghost_rigth_3.png')]

# ****BLOQUES
STYLE_SHEET_BLOQUES_JUEGO = "border: 1px solid; background-color: #1f1f1f"
PATH_BORDE = ['sprites', 'Elementos', 'bordermap.png']
PATH_PARED = ['sprites', 'Elementos', 'wall.png']
PATH_ROCA = ['sprites', 'Elementos', 'rock.png']
PATH_FUEGO = ['sprites', 'Elementos', 'fire.png']
PATH_ESTRELLA = ['sprites', 'Elementos', 'osstar.png']

# **** SONIDOS
PATH_SONIDO_GANAR = ['sounds', 'stageClear.wav']
PATH_SONIDO_PERDER = ['sounds', 'gameOver.wav']

# **** MAPAS
PATH_CARPETA_MAPAS = ['mapas']


# **********************************************************
# ******************* PARAMETROS PROPIOS *******************
# **********************************************************

VELOCIDAD_LUIGI = 0.075

# Se sugiere no editar los parametros a continuacion
# En caso de ser un str del titulo de una ventan, texto deun boton
# o algun tipo de mensaje, entonces es proablemente editable

# ****GENERALES ****
PIXELES_CASILLA: int = 32
PIXELES_MOVER: int = 1  # Cuantos pixeles se mueve la entendidad con mover()
CAMBIO_SPRITE: int = 4  # Pixeles cambia un sprite (multiplos de 2)
MODO_CONSTRUCTOR: str = "*** MODO CONSTRUCTOR ***"
POSICION_INICIAL: tuple = (0, 0)
LUIGI: int = 'L'
FANTASMA_V: int = 'V'
FANTASMA_H: int = 'H'
PARED: int = 'P'
ROCA: int = 'R'
FUEGO: int = 'F'
ESTRELLA: int = 'S'
FOLLOWER: int = 'Q'
DICT_MAXIMO_OBJETOS: dict = {LUIGI: 1,
                             FANTASMA_V: MAXIMO_FANTASMAS_VERTICAL,
                             FANTASMA_H: MAXIMO_FANTASMAS_HORIZONTAL,
                             FOLLOWER: MAXIMO_FOLLOWER_VILLAIN,
                             PARED: MAXIMO_PARED,
                             ROCA: MAXIMO_ROCA,
                             FUEGO: MAXIMO_FUEGO,
                             ESTRELLA: 1}
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
FRONT = 'front'


# ***VENTANA DE INICIO
TITULO_VENTANA_INICIO: str = "Ventana de Inicio"
POSICION_VENTANA_INICIO: tuple = (100, 100)
TAMANO_VENTANA_INICIO: tuple = (600, 680)
# **LOGO
TAMANO_LOGO: tuple = (518, 95)
# **ETIQUETA NOMBRE
TEXTO_ETIQUETA_NOMBRE: str = "Username"
TAMANO_ETIQUETA_NOMBRE: tuple = (100, 100)
STYLE_SHEET_ETIQUETA_NOMBRE: str = "color: white;"
# **CUADRO TEXTO
TAMANO_CUADRO_TEXTO: tuple = (300, 50)
# **BOTON LOGIN
TEXTO_BOTON_LOGIN: str = "Login"
TAMANO_BOTON_LOGIN: tuple = (100, 50)
# **BOTON SALIR
TEXTO_BOTON_SALIR_INICIO: str = "Salir"
TAMANO_BOTON_SALIR_INICIO: tuple = (100, 50)
#
ESPACIADO_VENTANA_INICIO: int = 15

# ***VENTANA DE JUEGO
TITULO_VENTANA_JUEGO: str = "Ventana de Juego"
POSICION_VENTANA_JUEGO: tuple = (100, 100)
TAMANO_VENTANA_JUEGO: tuple = (600, 600)

# **POPUPS FIN DEL JUEGO
TITULO_POPUP_GANAR: str = "Felicitaciones"
MENSAJE_GANAR: str = "\nFELICITACIONES GANASTE!\nTu Puntaje es: "
TITULO_POPUP_PERDER: str = "GAME OVER"
MENSAJE_PERDER: str = "\n- GAME OVER --"
TEXTO_BOTON_SALIR: str = 'Salir'
TEXTO_BOTON_VOLVER: str = 'Volver a Jugar'
MENSAJE_PERDER_TIEMPO: str = '\nSe te acabo el tiempo'
MENSAJE_PERDER_VIDAS: str = '\nNo te quedan vidas'

# POPUP ERROR NOMBRE
TITULO_POPUP_ERROR_NOMBRE: str = "ERROR NOMBRE"
MENSAJE_ERROR_NOMBRE_VACIO = "Nombre no insertado"
MENSAJE_ERROR_NOMBRE_ALFANUM = "El nombre ingresado no es alfanumerico"
MENSAJE_ERROR_NOMBRE_MAX = "Nombre muy largo, el maximo de caracteres: "
MENSAJE_ERROR_NOMBRE_MIN = "Nombre muy corto, el minimo de caracteres: "
# POPUP ERROR DROP
TITULO_POPUP_ERROR_DROP = "ERROR DROP"
MENSAJE_ERROR_DROP_INSUFICIENTES = 'No quedan objetos del tipo pedido'
MENSAJE_ERROR_DROP_TOPE = 'Ya existe un objeto en dicha casilla'
MENSAJE_ERROR_DROP_INCORRECTO = 'Coloque el objeto en una casilla valida'
MENSAJE_ERROR_DROP_MAPA = 'Coloque el objeto en el mapa'

# CHEATCODES
COMBINACION_CHEATCODE1 = ["K", "I", "L"]
COMBINACION_CHEATCODE2 = ["I", "N", "F"]

# **** MAPA
ESPACIADO_MAPA: int = 0
MARGENES_MAPA: int = (0, 0, 0, 0)

# **** Panel_Lateral
# botones y etiquetas
TEXTO_ETIQUETA_TIEMPO = 'Tiempo: '
TEXTO_ETIQUETA_VIDAS = 'Vidas: '
TEXTO_BOTON_PAUSA_FALSE = 'Pausar'
TEXTO_BOTON_PAUSA_TRUE = 'Reanudar'
TEXTO_BOTON_LIMPIAR = 'Limpiar'
TEXTO_BOTON_JUGAR = 'Jugar'
# FILTRO
TEXTO_FILTRO_TODOS = 'Todos'
TEXTO_FILTRO_BLOQUES = 'Bloques'
TEXTO_FILTRO_ENTIDADES = 'Entidades'
ID_ENTIDADES_FILTRO = -1
STYLE_SHEET_OBJETOS_PANEL = "border: 0px solid; background-color: #00FFFFFF"
