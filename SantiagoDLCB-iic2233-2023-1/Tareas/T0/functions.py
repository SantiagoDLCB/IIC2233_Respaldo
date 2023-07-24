# Agregar los imports que estimen necesarios
from os import path
from collections import deque
from tablero import imprimir_tablero
from copy import deepcopy


#########################################################
# Funciones Pedidas


def cargar_tablero(nombre_archivo: str) -> list:
    ubicacion_archivo = path.join('Archivos', nombre_archivo)
    with open(ubicacion_archivo) as archivo:
        # lee el documento y guarda la primera linea sin saltos de linea
        linea1 = archivo.readlines()[0].strip('\n')
    lista = linea1.split(',')  # creamos lista con todos los elementos en str
    celdas = deque(lista)  # lista de elementos se convierte en cola
    n = int(celdas.popleft())  # obtiene dimensiones tablero
    tablero = [[celdas.popleft() for y in range(n)]
               for x in range(n)]  # construir el tablero
    return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    n = len(tablero)
    # obtiene una unica lista con todos los elementos ordenados
    elementos = [elemento for fila in tablero for elemento in fila]
    texto = ','.join(elementos)
    texto = str(n) + ','+texto  # se añade el tamaño del tablero
    # guardamos texto en el archivo que crearemos con el nombre pedido
    ubicacion_archivo = path.join('Archivos', nombre_archivo)
    with open(ubicacion_archivo, 'w') as archivo:
        print(texto, file=archivo, end='')


def verificar_valor_bombas(tablero: list) -> int:
    bomba_invalidas = 0
    for fila in tablero:
        for celda in fila:
            # nos aseguramos que la celda sea una bomba
            if celda not in 'T-':
                bomba = int(celda)
                # chequa si no se cumple la regla 2
                if bomba < 2 or bomba > (2*len(tablero))-1:
                    bomba_invalidas += 1
    return bomba_invalidas


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    celda = tablero[coordenada[0]][coordenada[1]]
    if celda in 'T-':
        return 0
    observados = obtener_observables(tablero, coordenada)
    observados_validos = []
    for direccion in observados:
        ciclo = True
        for x1, y1 in direccion:
            if tablero[x1][y1] != 'T' and ciclo:
                observados_validos.append((x1, y1))
            else:
                ciclo = False
    return 1 + len(observados_validos)


def verificar_tortugas(tablero: list) -> int:
    tortugas = obtener_tortugas(tablero)
    tortugas_juntas = set()
    for x, y in tortugas:
        casos_posibles = [(x+1, y), (x-1, y), (x, y+1),
                          (x, y-1)]  # casos tortugas juntas
        for posible_tortuga in casos_posibles:
            if posible_tortuga in tortugas:
                tortugas_juntas.add((x, y))
    return len(tortugas_juntas)


def solucionar_tablero(tablero: list) -> list:
    reglas = [verificar_valor_bombas(tablero), bombas_tapadas(tablero),
              verificar_tortugas(tablero), verificar_islas(tablero)]
    if reglas != [0, [], 0, False]:  # Reglas 2, 3, 4,5
        return None
    bombas_malas = obtener_bombas_malas(tablero)
    if bombas_malas == []:
        return tablero
    posibles = observables_posibles(tablero, bombas_malas[0])
    if posibles == [] or tortuga_malpuesta(tablero, bombas_malas[0]) is True:
        return None
    for coord in posibles:
        tablero_final = solucionar_tablero(colocar_tortuga(tablero, coord))
        if tablero_final is not None:
            return tablero_final


def verificar_islas(tablero: list) -> bool:
    no_tortugas = [(x, y) for x in range(len(tablero))
                   for y in range(len(tablero)) if tablero[x][y] != 'T']
    for x, y in no_tortugas:
        existen_aisladas = True
        cercanas = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for coord in cercanas:
            if coord in no_tortugas:
                existen_aisladas = False
        if existen_aisladas is True:
            return True
    return False

#########################################################
# Funciones Propias


def obtener_tortugas(tablero: list) -> list:
    # retorna lista de coordenadas donde hay una tortuga
    return [(x, y) for x in range(len(tablero))
            for y in range(len(tablero)) if tablero[x][y] == 'T']


def obtener_observables(tablero: list, coord: tuple):
    x, y = coord
    # se crean listas con las cordenadas de las celdas observadas
    # por cada bomba en cada direccion hasta topar con paredes
    arriba = [(indice, y) for indice in range(x)][::-1]
    abajo = [(indice, y) for indice in range(x+1, len(tablero))]
    izquierda = [(x, indice) for indice in range(y)][::-1]
    derecha = [(x, indice) for indice in range(y+1, len(tablero))]
    # conjunto de las celdas observadas
    observados = [izquierda, derecha, arriba, abajo]
    return observados


def observables_posibles(tablero: list, coord: tuple) -> list:
    # retorna todos los elemento que observa una bomba
    # en donde se podria poner una tortuga por regla 3
    lista = []
    observados = obtener_observables(tablero, coord)
    bombas = [(x, y) for x in range(len(tablero))
              for y in range(len(tablero)) if tablero[x][y] not in 'T-']
    tortugas = obtener_tortugas(tablero)
    for direccion in observados:
        lista += [elem for elem in direccion if elem
                  not in tortugas and elem not in bombas]
    return lista


def obtener_bombas_malas(tablero: list) -> list:
    # retorna lista de coordenadas de bombas que su alcance
    # no es igual a su numero
    bombas = [(x, y) for x in range(len(tablero))
              for y in range(len(tablero)) if tablero[x][y] not in 'T-']
    malas = []
    for x, y in bombas:
        if int(tablero[x][y]) != verificar_alcance_bomba(tablero, (x, y)):
            malas.append((x, y))
    return malas


def bombas_tapadas(tablero: list) -> list:
    # Verifica si es que hay una T en el mismo espacio que una bomba
    # retorna lista de todas las coordenadas que no cumplen la regla 3
    tapadas = [(x, y) for x in range(len(tablero))
               for y in range(len(tablero)) if 'T' in tablero[x][y] and
               len(tablero[x][y]) != 1]
    return tapadas


def colocar_tortuga(tablero: list, coord: tuple) -> list:
    # coloca tortuga en coordenada especifica en un tablero duplicado
    x, y = coord
    tablero_nuevo = deepcopy(tablero)
    tablero_nuevo[x][y] = 'T'
    return tablero_nuevo


def tortuga_malpuesta(tablero: list, bomba_mala: tuple) -> bool:
    # Testea si es que al poner la tortuga el alcance es menor al de la bomba
    x, y = bomba_mala
    if verificar_alcance_bomba(tablero, bomba_mala) < int(tablero[x][y]):
        return True
    else:
        return False


if __name__ == "__main__":
    tablero_2x2 = [
        ['-', '2'],
        ['-', '-']
    ]
    resultado = verificar_valor_bombas(tablero_2x2)
    print(resultado)  # Debería ser 0

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 3

    tablero_resuelto = solucionar_tablero(tablero_2x2)

    print(tablero_resuelto)

    tablero_2x2_sol = [
        ['T', '2'],
        ['-', '-']
    ]

    resultado = verificar_alcance_bomba(tablero_2x2_sol, (0, 1))
    print(resultado)  # Debería ser 2

    resultado = verificar_tortugas(tablero_2x2_sol)
    print(resultado)  # Debería ser 0

    # EJEMPLOS DE PRUEBA
    # tablero = cargar_tablero('5x5.txt')
    # imprimir_tablero(tablero, False)
    # imprimir_tablero(solucionar_tablero(tablero), False)

    # tablero_ejemplo = [
    #     ["-", "2", "6", "-", "-", "-", "3"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["3", "-", "-", "5", "-", "-", "4"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["2", "-", "-", "-", "7", "4", "-"],
    # ]
    # tablero_ejemplo_sol = [
    #     ["T", "2", "6", "T", "-", "-", "3"],
    #     ["-", "T", "-", "-", "-", "-", "T"],
    #     ["-", "-", "-", "-", "T", "-", "-"],
    #     ["3", "T", "-", "5", "-", "T", "4"],
    #     ["T", "-", "-", "T", "-", "-", "-"],
    #     ["-", "-", "T", "-", "-", "T", "-"],
    #     ["2", "T", "-", "-", "7", "4", "T"],
    # ]
    # print(solucionar_tablero(tablero_ejemplo) == tablero_ejemplo_sol)
    # imprimir_tablero(tablero_ejemplo, False)
    # imprimir_tablero(solucionar_tablero(tablero_ejemplo), False)
