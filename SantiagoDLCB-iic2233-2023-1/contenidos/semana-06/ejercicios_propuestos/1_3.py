import threading
import time


def cuenta_3():
    for i in range(1, 40, 3):
        print(f"Contando de a 3: {i}")
        time.sleep(1)
    print("-- ¡Terminó cuenta 3! --")


def cuenta_2():
    thread = threading.Thread(target=cuenta_3)
    thread.start()
    thread.join()
    for i in range(1, 9, 2):
        print(f"Contando de a 2: {i}")
        time.sleep(2)
    print("-- ¡Terminó cuenta 2! --")


def cuenta_1():
    thread = threading.Thread(target=cuenta_2)
    thread.start()
    thread.join()
    for i in range(1, 9):
        print(f"Contando de a 1: {i}")
        time.sleep(3)
    print("-- ¡Terminó cuenta 1! --")


thread = threading.Thread(target=cuenta_1)
thread.start()
print("¡Todos terminaron en orden!")
