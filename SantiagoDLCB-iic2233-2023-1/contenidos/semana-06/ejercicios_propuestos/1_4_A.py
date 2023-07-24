import time
import random
from threading import Thread


# Implementar modelacion con Thread...
# ... puedes usar herencia si quieres ;)
class Minero(Thread):

    def __init__(self, nombre):
        # Completar clase
        super().__init__(name=nombre)
        self.nombre = nombre
        self.velocidad = random.randint(2, 4)
        self.cantidad = 0
        self.adentro = False
        pass

    def recolectar_recursos(self):
        cantidad = random.randint(5, 15)
        tiempo = cantidad/self.velocidad
        self.adentro = True
        time.sleep(tiempo)
        print(
            f'Trabajador {self.nombre} ha recolectado {cantidad} DCCriptoMonedas')
        self.cantidad += cantidad
        self.adentro = False

    def run(self):
        # Completar metodo
        for i in range(3):
            print(f'Trabajador {self.nombre} ha entrado a la DCCueva')
            self.recolectar_recursos()
        pass


t1 = Minero('John')  # Eres libre de modificar los nombres
t2 = Minero('Alex')  # Eres libre de modificar los nombres
t3 = Minero('Peter')  # Eres libre de modificar los nombres :)

# Acá debes iniciar los threads
t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# No modificar
total = t1.cantidad + t2.cantidad + t3.cantidad
print('------------------------------------------')
print(f'Se han recolectado {total} DCCriptoMonedas')
