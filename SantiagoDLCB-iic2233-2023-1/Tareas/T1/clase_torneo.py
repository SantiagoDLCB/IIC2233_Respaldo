from parametros import (METROS_META, DIAS_TOTALES_TORNEO, PROB_INICIAR_EVENTO,
                        PROB_LLUVIA, PROB_TERREMOTO, PROB_DERRUMBE,
                        METROS_PERDIDOS_DERRUMBE, FELICIDAD_PERDIDA)
import random
from clase_item import Consumible, Tesoro
from clase_excavador import nuevo_excavador
from clase_arena import Arena, arena_inicial_random


class Torneo:
    def __init__(self, ArenaInicial: Arena, equipo: list, mochila: list,
                 metros_cavados: float, dias_transcurridos: int) -> None:
        self.arena = ArenaInicial
        self.eventos = ['Lluvia', 'Terremoto', 'Derrumbe']
        self.equipo = equipo
        self.mochila = mochila
        self.__metros_cavados = metros_cavados
        self.meta: float = METROS_META
        self.dias_transcurridos = dias_transcurridos
        self.dias_totales: int = DIAS_TOTALES_TORNEO

    @property
    def metros_cavados(self):
        return self.__metros_cavados

    @metros_cavados.setter
    def metros_cavados(self, nuevos_metros_cavados):
        self.__metros_cavados = round(nuevos_metros_cavados, 2)

    def simular_dia(self):
        self.dias_transcurridos += 1  # sumar dia
        descansando = []
        excavaciones = []
        metros_totales_dia = 0
        items = []
        print(f'Día {self.dias_transcurridos}'.center(53),
              53*'-', 'Metros Cavados:', sep='\n')
        # Se obtienen valores aleatorios para arena magnetica
        if self.arena.tipo == 'magnetica':
            self.arena.humedad = random.randint(1, 10)
            self.arena.dureza = random.randint(1, 10)

        for excavador in self.equipo:
            if excavador.descanso_restante != 0:
                excavador.descanso_restante -= 1
                descansando.append(excavador)
            else:
                # Cavar
                metros = excavador.cavar(self.arena)
                excavaciones.append([excavador, metros])
                excavador.gastar_energia()
                metros_totales_dia += metros
                metros_totales_dia = round(metros_totales_dia, 2)

                # Encontrar items
                item_encontrado = excavador.encontrar_item(self.arena)
                items.append([excavador, item_encontrado])
                if item_encontrado is not None:
                    self.mochila.append(item_encontrado)
        self.metros_cavados += metros_totales_dia
        for excavacion in excavaciones:
            print(excavacion[0].nombre, 'ha cavado', excavacion[1], 'metros.')

        print(f'El equipo ha conseguido excavar {metros_totales_dia} metros',
              '\nItems Encontrados:', sep='\n')
        for item in items:
            if item[1] is None:
                print(item[0].nombre, 'no consiguió nada.')
            else:
                print(item[0].nombre, 'consiguió', item[1].nombre,
                      f'del tipo {item[1].tipo}.')

        # EVENTO
        if random.random() < PROB_INICIAR_EVENTO:
            self.iniciar_evento()
        if descansando == []:
            print('\nNingun excavador decidió descansar.')
        else:
            print('\n')
            for cansado in descansando:
                print(cansado.nombre, 'decidió descansar...')
        input('\n\nPresione enter para volver')

    def mostrar_estado(self):
        separador = 61*'-'
        print('*** Estado Torneo ***'.center(61), separador,
              f'Día actual: {self.dias_transcurridos+1}',
              f'Tipo de arena: {self.arena.tipo}',
              f'Metros excavados: {self.metros_cavados} / {self.meta}',
              separador,
              'Excavadores'.center(61),
              separador,
              'Nombre | Tipo | Energía | Fuerza | Suerte | Felicidad'
              .center(61), separador, sep='\n')
        for excavador in self.equipo:
            print(excavador.nombre, excavador.tipo, excavador.energia,
                  excavador.fuerza, excavador.suerte, excavador.felicidad,
                  sep=' | ')
        input('\n\nPresione enter para volver')

    def ver_mochila(self):
        separador = 86 * '-'
        print('*** Menú Ítems ***'.center(86),
              separador,
              'Nombre | Tipo | Descripción'.center(86),
              separador,
              sep='\n')
        c = 0
        for item in self.mochila:
            c += 1
            print(f'[{c}] {item.nombre}', item.tipo, item.descripcion,
                  sep=' | ')
        print(separador)

    def usar_consumible(self, Consumible1: Consumible) -> None:
        for Excavador1 in self.equipo:
            Excavador1.consumir(Consumible1)

    def abrir_tesoro(self, Tesoro1: Tesoro):
        if Tesoro1.calidad == 1:
            ExcavadorNuevo = nuevo_excavador(self, Tesoro1.cambio)
            if ExcavadorNuevo is None:
                print('\nNo existen trabajadores nuevos de tipo',
                      Tesoro1.cambio, 'para agregar.')
                print('Has malgastado tu tesoro.')
            else:
                self.equipo.append(ExcavadorNuevo)
                print(f'\nSe agrego *' + ExcavadorNuevo.nombre + '* de tipo *'
                      + ExcavadorNuevo.tipo, '* a tu equipo')
        elif Tesoro1.calidad == 2:
            if Tesoro1.cambio != self.arena.tipo:
                nombre_viejo = self.arena.nombre
                tipo_viejo = self.arena.tipo
                nueva_arena = arena_inicial_random(Tesoro1.cambio)
                self.arena = nueva_arena
                print(f'\nSe cambio la arena del torneo *{nombre_viejo}*',
                      f'de tipo *{tipo_viejo}* a *{self.arena.nombre}*',
                      f'de tipo *{self.arena.tipo}*.')
            else:
                print(f'\nLa arena actual ya es de tipo *{self.arena.tipo}*')
                print('Has malgastado tu tesoro.')

    def iniciar_evento(self):
        probabilidades = [PROB_LLUVIA, PROB_TERREMOTO, PROB_DERRUMBE]
        aleatorio = random.choices(self.eventos, probabilidades, k=1)[0]
        print(f'\n¡¡Durante el día de trabajo ocurrió el evento {aleatorio}!!')
        if aleatorio == 'Lluvia':
            if self.arena.tipo == 'normal':
                nueva_arena = arena_inicial_random('mojada')
                self.arena = nueva_arena
            elif self.arena.tipo == 'rocosa':
                nueva_arena = arena_inicial_random('magnetica')
                self.arena = nueva_arena
        elif aleatorio == 'Terremoto':
            if self.arena.tipo == 'normal':
                nueva_arena = arena_inicial_random('rocosa')
                self.arena = nueva_arena
            elif self.arena.tipo == 'mojada':
                nueva_arena = arena_inicial_random('magnetica')
                self.arena = nueva_arena
        elif aleatorio == 'Derrumbe':
            nueva_arena = arena_inicial_random('normal')
            self.arena = nueva_arena
            self.metros_cavados -= METROS_PERDIDOS_DERRUMBE
            print(f'El equipo perdio', METROS_PERDIDOS_DERRUMBE,
                  'metros de progreso')
        for excavador in self.equipo:
            excavador.felicidad -= FELICIDAD_PERDIDA
        print(f'Tu equipo ha perdido {FELICIDAD_PERDIDA} de felicidad')
