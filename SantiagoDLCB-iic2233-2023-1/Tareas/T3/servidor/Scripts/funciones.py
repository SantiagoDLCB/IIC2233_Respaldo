import json
import os
import random
with open(os.path.join('parametros.json')) as archivo:
    PARAMETROS = json.load(archivo)


def obtener_id_jugador(id_usados):
    ids_posibles = [id1 for id1 in PARAMETROS["ID_POSIBLES"]
                    if id1 not in id_usados]
    return random.choice(ids_posibles)


def imprimir_logs(evento: str, cliente: str = "-",
                  detalles: str = PARAMETROS["LOG_SECCION_VACIA"]):
    n = PARAMETROS["LOG_ANCHO_TEXTO"]
    separa = PARAMETROS["LOG_SEPARADOR"]
    vacio = PARAMETROS["LOG_SECCION_VACIA"]
    print(cliente.center(n), evento.center(n), detalles.center(n), sep=separa)
    print(vacio*n, vacio*n, vacio*n, sep=separa)
