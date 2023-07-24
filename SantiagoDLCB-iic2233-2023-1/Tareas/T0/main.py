from os import path, system
from sys import exit
from functions import (cargar_tablero, verificar_valor_bombas,
                       verificar_tortugas, guardar_tablero, verificar_islas,
                       obtener_bombas_malas, bombas_tapadas,
                       solucionar_tablero)
from tablero import imprimir_tablero


def menu_inicio():
    print('*** Menú de Inicio ***')
    archivo = input('Indique el nombre del archivo que desea abrir'
                    ' (recuerde incluir la extensión): ')
    camino = path.join('Archivos', archivo)
    system('cls')
    if path.exists(camino) is False or archivo == '':
        print('\nArchivo incorrecto, vuelva a ejecutar el programa'
              ' para intentarlo nuevamente \n')
        exit()
    menu_acciones(archivo)


def menu_acciones(archivo):
    print('*** Menú de Acciones ***\n\n', '[1] Mostrar tablero',
          '[2] Validar tablero', '[3] Revisar solución',
          '[4] Solucionar tablero', '[5] Salir del programa', sep='\n')
    seleccion = input('\nSeleccione una opción: ')
    system('cls')
    menu = {'1': opcion1, '2': opcion2, '3': opcion3, '4': opcion4}
    if seleccion == '5':
        exit()
    elif seleccion not in menu.keys():
        print('Opcion Invalida: Asegurese de escribir un numero del 1 al 5\n')
    else:
        menu.get(seleccion)(archivo)
    input('\n\nPresione enter para volver al Menú de Acciones:\n')
    system('cls')
    menu_acciones(archivo)


def opcion1(archivo: list) -> None:
    tablero = cargar_tablero(archivo)
    imprimir_tablero(tablero)
    return


def opcion2(archivo: list) -> None:
    tablero = cargar_tablero(archivo)
    if (verificar_valor_bombas(tablero) != 0
            or verificar_tortugas(tablero) != 0):
        print('Tablero Inválido')
    elif verificar_islas(tablero) is True:
        print('Tablero Inválido')
    else:
        print('Tablero Válido')
    return


def opcion3(archivo: list) -> None:
    tablero = cargar_tablero(archivo)
    if (verificar_valor_bombas(tablero) != 0 or
            verificar_tortugas(tablero) != 0 or
            obtener_bombas_malas(tablero) != [] or
            bombas_tapadas(tablero) != []):
        print('Tablero Inválido')
    else:
        print('Tablero Válido')
    return


def opcion4(archivo: list) -> None:
    tablero = cargar_tablero(archivo)
    solucion = solucionar_tablero(tablero)
    if solucion is None:
        print('No hay solución que cumpla todas las reglas')
    else:
        print('Aqui esta la solución\n')
        imprimir_tablero(solucion)
        lista_nombre = archivo.split('.')
        nuevo_nombre = '.'.join(lista_nombre[:-1])+'_sol.'+lista_nombre[-1]
        guardar_tablero(nuevo_nombre, solucion)
    return


def menu_inicio():
    print('*** Menú de Inicio ***')
    archivo = input('Indique el nombre del archivo que desea abrir'
                    ' (recuerde incluir la extensión): ')
    camino = path.join('Archivos', archivo)
    system('cls')
    if path.exists(camino) is False or archivo == '':
        print('\nArchivo incorrecto, vuelva a ejecutar el programa'
              ' para intentarlo nuevamente \n')
        exit()
    menu_acciones(archivo)


def menu_acciones(archivo):
    print('*** Menú de Acciones ***\n\n', '[1] Mostrar tablero',
          '[2] Validar tablero', '[3] Revisar solución',
          '[4] Solucionar tablero', '[5] Salir del programa', sep='\n')
    seleccion = input('\nSeleccione una opción: ')
    system('cls')
    menu = {'1': opcion1, '2': opcion2, '3': opcion3, '4': opcion4}
    if seleccion == '5':
        exit()
    elif seleccion not in menu.keys():
        print('Opcion Invalida: Asegurese de escribir un numero del 1 al 5\n')
    else:
        menu.get(seleccion)(archivo)
    input('\n\nPresione enter para volver al Menú de Acciones:\n')
    system('cls')
    menu_acciones(archivo)


menu_inicio()
