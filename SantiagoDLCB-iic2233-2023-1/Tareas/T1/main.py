import os
from clase_torneo import Torneo
from clase_item import Consumible, Tesoro
from clase_excavador import excavadores_inicial_random
from clase_arena import arena_inicial_random
from funciones import guardar_partida, cargar_partida
from parametros import ARENA_INICIAL, CANTIDAD_EXCAVADORES_INICIALES


def menu_inicio():
    salir = False
    while salir is not True:
        os.system('cls')
        print('*** Menú de Inicio ***',
              '----------------------',
              '[1] Nueva partida',
              '[2] Cargar partida',
              '[X] Salir del programa', sep='\n')
        opcion = input('Indique su opción (1, 2 o X): ')
        if opcion == '1':
            Arena_actual = arena_inicial_random(ARENA_INICIAL)
            excavadores = excavadores_inicial_random(
                CANTIDAD_EXCAVADORES_INICIALES)
            # inicio menu principal
            TorneoInicial = Torneo(Arena_actual, excavadores, [], 0, 0)
            salir = menu_principal(TorneoInicial)
        elif opcion == '2':
            resultado_carga = menu_de_carga()
            if type(resultado_carga) == bool and resultado_carga is True:
                salir = True
            elif type(resultado_carga) == str:
                nombre_archivo = resultado_carga
                camino = os.path.join('Partidas', nombre_archivo + '.txt')
                TorneoInicial = cargar_partida(camino)
                salir = menu_principal(TorneoInicial)
        elif opcion == 'X':
            salir = True
        else:
            print('Opcion incorrecta, porfavor ingrese una opción valida.\n\n')


def menu_principal(TorneoActual: Torneo) -> (bool | None):
    volver_inicio = False
    salir = False
    while (volver_inicio is not True and
           TorneoActual.dias_transcurridos < TorneoActual.dias_totales):
        os.system('cls')
        transcurridos = TorneoActual.dias_transcurridos + 1
        totales = TorneoActual.dias_totales
        print('*** Menú Principal ***',
              '---------------------------',
              f'Día torneo DCCavaCava: {transcurridos}/{totales}',
              f'Tipo de arena: {TorneoActual.arena.tipo}',
              '[1] Simular día torneo',
              '[2] Ver estado torneo',
              '[3] Ver ítems',
              '[4] Guardar partida',
              '[Z] Volver',
              '[X] Salir del programa', sep='\n')
        opcion = input('Indique su opción (1, 2, 3, 4, Z o X): ')
        os.system('cls')
        if opcion == '1':
            TorneoActual.simular_dia()
        elif opcion == '2':
            TorneoActual.mostrar_estado()
        elif opcion == '3':
            salir = menu_items(TorneoActual)
        elif opcion == '4':
            guardar_partida(TorneoActual)
        elif opcion == 'Z':
            volver_inicio = True  # volver menu_inicio
        elif opcion == 'X':
            salir = True  # Salir
        else:
            print('Opcion incorrecta, porfavor ingrese una opción valida.\n\n')
            input('\n\nPresione enter para volver')
        if salir is True:
            return True
    if TorneoActual.dias_transcurridos >= TorneoActual.dias_totales:
        os.system('cls')
        print(f'Cavaste: {TorneoActual.metros_cavados} metros',
              f'y la meta era {TorneoActual.meta} metros.')
        if TorneoActual.metros_cavados < TorneoActual.meta:
            print('\n\n'+'PERDISTE'.center(50, '-')+'\n')
        else:
            print('\n\n'+'GANASTE'.center(50, '-')+'\n')
        input('\n\nPresione enter para volver')


def menu_items(TorneoActual: Torneo) -> (bool | None):
    os.system('cls')
    volver_menu_principal = False
    while volver_menu_principal is not True:
        os.system('cls')
        TorneoActual.ver_mochila()
        numero = len(TorneoActual.mochila)
        print('[Z] Volver',
              '[X] Salir del programa',
              sep='\n')
        texto = ', '.join([str(x+1) for x in range(numero)]+['Z'])
        opcion = input('Indique su opción ('+texto+' o X): ')
        opciones_consumibles = {str(num+1): TorneoActual.mochila[num]
                                for num in range(numero)}
        if opcion == 'X':
            return True  # Salir
        elif opcion == 'Z':
            volver_menu_principal = True
        elif opcion in opciones_consumibles.keys():
            os.system('cls')
            indice = int(opcion)-1
            ItemElegido = TorneoActual.mochila.pop(indice)
            if type(ItemElegido) == Consumible:
                TorneoActual.usar_consumible(ItemElegido)
                print(f'\nEl equipo consumio *{ItemElegido.nombre}*',
                      'el cual les', ItemElegido.descripcion)
                input('\n\nPresione enter para volver')
            elif type(ItemElegido) == Tesoro:
                TorneoActual.abrir_tesoro(ItemElegido)
                input('\n\nPresione enter para volver')
        else:
            os.system('cls')
            print('Opcion incorrecta, porfavor ingrese una opción valida.\n\n')
            input('\n\nPresione enter para volver')


def menu_de_carga() -> (str | bool | None):
    volver_menu_principal = False
    while volver_menu_principal is not True:
        os.system('cls')
        archivos = os.listdir(os.path.join('Partidas'))
        n = len(archivos)
        dict_opciones = {str(i+1): archivos[i][:-4] for i in range(n)}
        print('*** Menú de carga ***', 22*'-', sep='\n')
        for num in dict_opciones:
            print(f'[{num}] {dict_opciones[num]}')
        print('[Z] Volver',
              '[X] Salir del programa',
              sep='\n')
        texto = ', '.join([str(x+1) for x in range(n)]+['Z'])
        opcion = input('Indique su opción ('+texto+' o X): ')
        if opcion == 'X':
            return True  # Salir
        elif opcion == 'Z':
            volver_menu_principal = True
        elif opcion in dict_opciones.keys():
            return dict_opciones[opcion]
        else:
            os.system('cls')
            print('Opcion incorrecta, porfavor ingrese una opción valida.\n\n')
            input('\n\nPresione enter para volver')


menu_inicio()
