import threading
import time
from collections import deque
from random import randint


clientes = {
    "Enzo": [],
    "Dani": [],
    "Dante": [],
    "Josefina": [],
    "Ian": []
}
cola_de_pedidos = deque([("Enzo", "🍕"), ("Josefina", "🍣"), ("Dante", "🌭"), ("Dani", "🍟"), ("Ian", "🍔"),
                         ("Ian", "🍰"), ("Enzo", "🌮"), ("Dani", "🍩"), ("Enzo", "🍫")])
lock_tomar_pedido = threading.Lock()

def atender_pedidos(cola, clientes):
    while len(cola) > 0:
        lock_tomar_pedido.acquire()
        print("¡Haré un pedido!")
        cliente, comida = cola[0]
        print(f"Preparando {comida} para {cliente}")
        time.sleep(1)
        if randint(0, 1) == 1:
            bandeja = clientes[cliente]
            bandeja.append(comida)
            print(f"Pedido de {comida} entregado a {cliente}")
            cola.popleft()
        else:
            print("¡Se me cayó!")
        lock_tomar_pedido.release()
        

trabajador_1 = threading.Thread(target=atender_pedidos, args=(cola_de_pedidos, clientes))
trabajador_2 = threading.Thread(target=atender_pedidos, args=(cola_de_pedidos, clientes))
trabajador_3 = threading.Thread(target=atender_pedidos, args=(cola_de_pedidos, clientes))


trabajador_1.start()
trabajador_2.start()
trabajador_3.start()


trabajador_1.join()
trabajador_2.join()
trabajador_3.join()

for cliente in clientes:
    print(f"La bandeja de {cliente} tiene: {clientes[cliente]}")
