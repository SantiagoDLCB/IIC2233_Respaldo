from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        string = json.dumps(dictionary)
        codificado = string.encode("UTF-8")
        return bytearray(codificado)

    except (TypeError) as error:
        raise JsonError()


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:

    mas_grande = sorted(secuencia)[-1]
    if mas_grande >= len(mensaje):
        raise SequenceError()
    x = set()
    for i in secuencia:
        if i in x:
            raise SequenceError()
        else:
            x.add(i)
    return None


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    t = b''
    for i in secuencia:
        i = i.to_bytes(2, byteorder="big")
        t += i
    return bytearray(t)


def codificar_largo(largo: int) -> bytearray:
    n = largo.to_bytes(4, byteorder="big")
    return bytearray(n)


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()

    for i in range(len(mensaje)):
        if i not in secuencia:
            m_reducido += mensaje[i:i+1]
    for i in secuencia:
        m_bytes_secuencia += mensaje[i:i+1]

    return [m_bytes_secuencia, m_reducido]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
