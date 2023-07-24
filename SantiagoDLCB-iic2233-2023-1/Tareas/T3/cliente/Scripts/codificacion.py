import json
import os
with open(os.path.join('parametros.json')) as archivo:
    PARAMETROS = json.load(archivo)


def codificar_mensaje(mensaje: bytearray):
    CHUNK_SIZE = PARAMETROS["CHUNK_SIZE"]
    mensaje_codificado = bytearray(len(mensaje).to_bytes(4, 'little'))
    n_chunk = -1
    for n_chunk in range(len(mensaje)//CHUNK_SIZE):
        mensaje_codificado += bytearray(n_chunk.to_bytes(4, 'big'))
        mensaje_codificado += mensaje[n_chunk *
                                      CHUNK_SIZE: (n_chunk+1)*CHUNK_SIZE]
    if len(mensaje) % CHUNK_SIZE != 0:
        n_chunk += 1
        mensaje_codificado += bytearray(n_chunk.to_bytes(4, 'big'))
        mensaje_codificado += mensaje[n_chunk * CHUNK_SIZE:]
        for vacio in range(CHUNK_SIZE - (len(mensaje) % CHUNK_SIZE)):
            mensaje_codificado += bytearray(b'\x00')
    return mensaje_codificado


def decodificar_mensaje(mensaje: bytearray):
    CHUNK_SIZE = PARAMETROS["CHUNK_SIZE"]
    largo = int.from_bytes(mensaje[:4], 'little')
    chunks = mensaje[4:]
    decodificado = bytearray()
    chunks_totales = largo//CHUNK_SIZE
    if largo % CHUNK_SIZE != 0:
        chunks_totales += 1
    for chunk in range(chunks_totales):
        decodificado += chunks[4: 4+CHUNK_SIZE]
        chunks = chunks[4+CHUNK_SIZE:]
    decodificado = decodificado[:largo]
    return decodificado
