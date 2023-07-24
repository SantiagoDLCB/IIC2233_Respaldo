import parametros as p


def checkear_tope_roca(x, y, direccion, lista_rocas, lista_paredes_fantasmas):
    """Retorna True si la choca con roca y esta no se puede mover\n
        Retorna False si choca con roca y esta se mueve\n
        Retorna None si no choca con rocas"""
    if checkear_tope(x, y, direccion, lista_rocas):
        x2, y2 = nueva_posicion(x, y, direccion)
        if checkear_tope(x2, y2, direccion,
                         lista_paredes_fantasmas + lista_rocas):
            return True
        return False
    return None


def checkear_tope(x, y, direccion, lista_paredes):
    """Revisa si la entidad va a topar con algo si se mueve en una direccion \n
        Retorna True si topa y retorna False si no topa"""
    if nueva_posicion(x, y, direccion) in lista_paredes:
        return True
    False


def nueva_posicion(x, y, direccion):
    """Entrega la nueva posicion de un objeto si se mueve en una direccion"""
    pixeles = p.PIXELES_CASILLA
    mov_y = {"up": -pixeles, "down": pixeles, "right": 0, "left": 0}
    mov_x = {"up": 0, "down": 0, "right": pixeles, "left": -pixeles}
    nueva_posicion = (x + mov_x[direccion],
                      y + mov_y[direccion])
    return nueva_posicion


def generar_mapa_vacio():
    """Genera matriz equivalenete al mapa sin los bordes"""
    mapa = []
    for y in range(p.LARGO_GRILLA - 2):
        fila = []
        for x in range(p.ANCHO_GRILLA - 2):
            fila.append('-')
        mapa.append(fila)
    return mapa
