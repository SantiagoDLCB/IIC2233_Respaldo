
def encriptar(msg: bytearray, N: int) -> bytearray:
    c = 0
    while N > c:
        msg = msg[-1:] + msg[:-1]
        c += 1
    byte_0 = msg[0]
    byte_n = msg[N % len(msg)]
    msg[N % len(msg)] = byte_0
    msg[0] = byte_n
    return msg


def desencriptar(msg: bytearray, N: int):
    byte_0 = msg[0]
    byte_n = msg[N % len(msg)]
    msg[N % len(msg)] = byte_0
    msg[0] = byte_n
    c = 0
    while N > c:
        msg = msg[1:] + msg[:1]
        c += 1
    return msg


if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(
        b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(
        b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original, N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")

    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
