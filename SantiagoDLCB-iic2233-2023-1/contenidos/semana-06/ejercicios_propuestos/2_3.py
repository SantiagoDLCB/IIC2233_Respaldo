from threading import Thread, Event
from time import sleep
peticion = Event()
resuelta = Event()


class DCCueva(Thread):

    def __init__(self, peticion_suministros, peticion_resuelta):
        super().__init__()
        self.meses_trabajo = 5  # Puedes usar el valor que prefieras
        # Completar con sistema de señales
        self.peticion_suministros = peticion_suministros
        self.peticion_resuelta = peticion_resuelta

    def run(self):
        print(f"(DCCueva) ¡Comienzan operaciones en la DCCueva!")
        meses = 0
        while meses < self.meses_trabajo:
            meses += 1
            print(
                f'(DCCueva) Empezaré un nuevo mes, a pedir recursos (mes {meses})')
            self.peticion_suministros.set()
            self.peticion_resuelta.wait()
            self.peticion_resuelta.clear()
            for i in range(5):
                sleep(1)
                print(f'Utilizando recursos... {i+1}/5')


class SuperDrone(Thread):

    def __init__(self, peticion_suministros, peticion_resuelta):
        super().__init__()
        self.daemon = True
        self.peticion_suministros = peticion_suministros
        self.peticion_resuelta = peticion_resuelta

    def run(self):
        while True:
            print('(SuperDrone) Esperando una petición de suministros')
            self.peticion_suministros.wait()
            self.peticion_suministros.clear()
            print('(SuperDrone) Llegó una petición de suministros, a trabajar')
            for i in range(2):
                sleep(1)
                print(f'Resolviendo petición... {i+1}/2')
            self.peticion_resuelta.set()

            # Completar son sistema de señales
            # Nota: no importa que sea un loop infinito, es daemon thread.
            pass


# Completar con sistema de señales e instanciacion de threads
dccueva = DCCueva(peticion, resuelta)
drone = SuperDrone(peticion, resuelta)
dccueva.start()
drone.start()
