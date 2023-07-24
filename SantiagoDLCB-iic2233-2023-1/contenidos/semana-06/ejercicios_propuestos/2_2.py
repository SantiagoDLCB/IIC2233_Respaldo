import threading
import time
def jugar_nivel(nivel, evento_nivel):
    ##### SOLO AGREGAR CÓDIGO EN ESTA FUNCIÓN
    print(f"¡Jugando nivel {nivel}!")
    time.sleep(1)
    print(f"Batallando en el nivel {nivel}")
    time.sleep(3)
    print(f"Terminando el nivel {nivel}")
    evento_nivel.set()
    
    
evento_nivel_terminado = threading.Event()

n1 = threading.Thread(target=jugar_nivel, args=[1, evento_nivel_terminado])
n2 = threading.Thread(target=jugar_nivel, args=[2, evento_nivel_terminado])
n3 = threading.Thread(target=jugar_nivel, args=[3, evento_nivel_terminado])
n4 = threading.Thread(target=jugar_nivel, args=[4, evento_nivel_terminado])

# =========== SOLO AGREGAR CÓDIGO DESDE AQUÍ HACIA ABAJO =============

n1.start()
evento_nivel_terminado.wait()
evento_nivel_terminado.clear()
n2.start()
evento_nivel_terminado.wait()
evento_nivel_terminado.clear()
n3.start()
evento_nivel_terminado.wait()
n4.start()