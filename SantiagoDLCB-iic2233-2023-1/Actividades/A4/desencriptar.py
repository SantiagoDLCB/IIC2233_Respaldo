from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    # Completar
    try:
        string = mensaje_codificado.decode("UTF-8")
        dictionary = json.loads(string)
        return dictionary

    except json.JSONDecodeError:
        raise JsonError


def decodificar_largo(mensaje: bytearray) -> int:
    # Completar
    n = int.from_bytes(mensaje[0:4], byteorder="big")
    return n


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    secuencia_codificada = bytearray()
    # Completar
    largo = decodificar_largo(mensaje)
    m_bytes_secuencia += mensaje[4: 4 + largo]
    secuencia_codificada += mensaje[-2*largo:]
    m_reducido += mensaje[4 + largo: -2*largo]

    return [m_bytes_secuencia, m_reducido, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    # Completar
    lista = []
    for i in range(len(secuencia_codificada)//2):
        n = int.from_bytes(secuencia_codificada[i*2:i*2+2], byteorder='big')
        lista.append(n)
    return lista


def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    lista = separar_msg_encriptado(mensaje)
    secuencia = decodificar_secuencia(lista[2])
    m_bytes_secuencia = lista[0]
    m_reducido = lista[1]
    m_final = bytearray()
    print(secuencia)
    lista = [None for x in range(len(m_reducido+m_bytes_secuencia))]
    for i in range(len(secuencia)):
        lista[secuencia[i]] = m_bytes_secuencia[i]

    c = 0
    for i in range(len(lista)):
        if lista[i] is None:
            lista[i] = m_reducido[c]
            c += 1

    return bytearray(lista)


if __name__ == "__main__":
    mensaje = bytearray(
        b'\x00\x00\x00\x04"a}a{tm": 1\x00\x01\x00\x05\x00\n\x00\x03')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
