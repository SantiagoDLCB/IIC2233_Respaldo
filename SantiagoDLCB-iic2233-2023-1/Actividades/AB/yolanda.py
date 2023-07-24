import api
import re
import requests
import time


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        # TODO: Completar
        self.regex_validador_fechas = "^(\d{1,2})\sde\s[a-zA-Z]+\sde\s((20\d\d)|(19\d\d)|\d\d)$"
        # TODO: Completar
        self.regex_extractor_signo = "L[o|a]{1}s\s+([a-zA-Z]+[s|S])\s+pueden\s+.+\."

    def saludar(self) -> dict:
        # TODO: Completar
        respuesta = requests.get(f"{self.base}/")
        dict1 = {"status-code": respuesta.status_code,
                 "saludo": respuesta.json()["result"]}
        return dict1

    def verificar_horoscopo(self, signo: str) -> bool:
        # TODO: Completar
        respuesta = requests.get(f"{self.base}/signos")
        signos = respuesta.json()["result"]
        return signo in signos

    def dar_horoscopo(self, signo: str) -> dict:
        # TODO: Completar
        param = {"signo": signo}
        respuesta = requests.get(f"{self.base}/horoscopo", param)
        dict1 = {"status-code": respuesta.status_code,
                 "mensaje": respuesta.json()["result"]}
        return dict1

    def dar_horoscopo_aleatorio(self) -> dict:
        # TODO: Completar
        respuesta = requests.get(f"{self.base}/aleatorio")
        if respuesta.status_code != 200:
            dict1 = {"status-code": respuesta.status_code,
                     "mensaje": respuesta.json()["result"]}
            return dict1
        else:
            respuesta2 = requests.get(respuesta.json()["result"])
            dict1 = {"status-code": respuesta2.status_code,
                     "mensaje": respuesta2.json()["result"]}
            return dict1

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        # TODO: Completar
        header = {'Authorization': access_token}
        datos = {"signo": signo, "mensaje": mensaje}
        res = requests.post(f"{self.base}/update", headers=header,
                            data=datos)
        if res.status_code == 401:
            return "Agregar horoscopo no autorizado"
        elif res.status_code == 400:
            return res.json()["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        # TODO: Completar
        header = {'Authorization': access_token}
        datos = {"signo": signo, "mensaje": mensaje}
        res = requests.put(f"{self.base}/update", headers=header,
                           data=datos)
        if res.status_code == 401:
            return "Editar horoscopo no autorizado"
        elif res.status_code == 400:
            return res.json()["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        # TODO: Completar
        header = {'Authorization': access_token}
        datos = {"signo": signo}
        res = requests.delete(f"{self.base}/remove", headers=header,
                              data=datos)
        if res.status_code == 401:
            return "Eliminar signo no autorizado"
        elif res.status_code == 400:
            return res.json()["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
