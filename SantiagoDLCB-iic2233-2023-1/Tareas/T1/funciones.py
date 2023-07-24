from clase_torneo import Torneo
from clase_item import Consumible, Tesoro, crear_item_tipo
from clase_excavador import crear_excavador_tipo
from clase_arena import crear_arena_tipo
import os


def guardar_partida(TorneoActual: Torneo) -> None:
    # ejecuta la opcion del menu principal y llama a escribir_archivo
    nombre_partida = input('Ingrese un nombre para guardar su partida: ')
    camino = os.path.join('Partidas', nombre_partida+'.txt')
    os.system('cls')
    if os.path.isfile(camino) is True:
        print(f'Ya existe una partida guardada en *{nombre_partida}*',
              'se sobrecribirá el archivo')
    escribir_archivo(camino, TorneoActual)
    print('Se guardo exitosamente la partida',
          f'en el archivo *{nombre_partida}*')
    input('\n\nPresione enter para volver')


def cargar_partida(ubicacion: str) -> Torneo:
    # abre el archivo indicado en la opcion 2 del menu de inicio
    with open(ubicacion, encoding='utf-8') as archivo:
        info = [linea.strip('\n') for linea in archivo.readlines()]
    # Se cargan los datos y se instancia la arena
    datos_arena = [int(dato) if dato.isnumeric()
                   else dato for dato in info[0].split(',')]
    tipo_arena = datos_arena[0]
    datos = datos_arena[1:]
    ArenaCargada = crear_arena_tipo(tipo_arena, datos)
    # Se cargan los datos, se instancian los excavadores y se guardan en equipo
    datos_excavadores = info[1].split(',,')
    datos_excavadores = [datos.split(',') for datos in datos_excavadores]
    equipo = []
    for datos_excavador in datos_excavadores:
        tipo = datos_excavador[0]
        datos = [int(dato) if dato.isnumeric()
                 else dato for dato in datos_excavador[1:]]
        equipo.append(crear_excavador_tipo(tipo, datos))
    # Se cargan los datos, se instancian los items y se guardan en mochila
    datos_items = info[2].split(',,')
    datos_items = [datos.split(',') for datos in datos_items]
    mochila = []
    for datos_item in datos_items:
        tipo = datos_item[0]
        if tipo == 'Consumible':
            datos = datos_item[1:3] + [int(dato)for dato in datos_item[3:]]
        else:
            datos = [int(dato) if dato.isnumeric()
                     else dato for dato in datos_item[1:]]
        if datos != []:
            mochila.append(crear_item_tipo(tipo, datos))
    # Se cargan el resto de atributos del torneo
    metros_cavados = float(info[3])
    dias_transcurridos = int(info[4])
    # se retorna el torneo a partir de los datos
    return Torneo(ArenaCargada, equipo, mochila, metros_cavados,
                  dias_transcurridos)


def escribir_archivo(ubicacion: str, TorneoActual: Torneo) -> None:
    # Escribe en el archivo indicado los datos del Torneo
    # Siguiendo el mismo formato que cargar_archivo()
    with open(ubicacion, 'w', encoding='utf-8') as archivo:
        print(TorneoActual.arena.tipo, TorneoActual.arena.nombre,
              TorneoActual.arena.rareza, TorneoActual.arena.humedad,
              TorneoActual.arena.dureza, TorneoActual.arena.estatica, sep=',',
              file=archivo)
        lista_excavadores = []
        for excavador in TorneoActual.equipo:
            datos = [excavador.tipo, excavador.nombre, excavador.edad,
                     excavador.energia, excavador.fuerza, excavador.suerte,
                     excavador.felicidad]
            datos = [str(dato) for dato in datos]
            lista_excavadores.append(','.join(datos))
        # Los excavadores se separan por doble comas y sus datos por una coma
        print(',,'.join(lista_excavadores), file=archivo)
        lista_items = []
        for item in TorneoActual.mochila:
            if type(item) == Consumible:
                datos = [item.tipo, item.nombre, item.descripcion,
                         item.energia, item.fuerza, item.suerte,
                         item.felicidad]
            elif type(item) == Tesoro:
                datos = [item.tipo, item.nombre, item.descripcion,
                         item.calidad, item.cambio]
            datos = [str(dato) for dato in datos]
            lista_items.append(','.join(datos))
        # Los items se separan por doble comas y sus datos por una coma
        print(',,'.join(lista_items), file=archivo)
        print(TorneoActual.metros_cavados, file=archivo)
        print(TorneoActual.dias_transcurridos, file=archivo)
