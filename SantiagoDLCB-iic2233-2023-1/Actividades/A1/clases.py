from abc import ABC, abstractmethod


class Animal(ABC):
    identificador = 0

    def __init__(self, peso, nombre, *args, **kwargs) -> None:
        self.peso = peso
        self.nombre = nombre
        self.__energia = 100
        self.identificador = Animal.identificador
        Animal.identificador += 1

    @abstractmethod
    def desplazarse(self) -> None:
        return

    @property
    def energia(self) -> int:
        return self.__energia

    @energia.setter
    def energia(self, valor) -> int:
        self.__energia = valor
        if self.__energia < 0:
            self.__energia = 0
    pass


class Terrestre(Animal, ABC):

    def __init__(self, cantidad_patas, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cantidad_patas = cantidad_patas

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 5

    def desplazarse(self) -> str:
        nueva = self.energia - self.energia_gastada_por_desplazamiento()
        self.energia = nueva
        return "caminando..."

    pass


class Acuatico(Animal, ABC):

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 2

    def desplazarse(self) -> str:
        nueva = self.energia - self.energia_gastada_por_desplazamiento()
        self.energia = nueva
        return "nadando..."

    pass


class Perro(Terrestre):

    def __init__(self, raza, *args, **kwargs) -> None:
        super().__init__(cantidad_patas=4, *args, **kwargs)
        self.raza = raza

    def ladrar(self) -> str:
        return "guau guau"

    pass


class Pez(Acuatico):
    def __init__(self, color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color

    def nadar(self) -> str:
        return "moviendo aleta"

    pass


class Ornitorrinco(Terrestre, Acuatico):

    def desplazarse(self) -> str:
        energia_acuatica = Acuatico.energia_gastada_por_desplazamiento(self)
        energia_terrestre = Terrestre.energia_gastada_por_desplazamiento(self)
        nueva_energia = self.energia - \
            round((energia_acuatica + energia_terrestre)/2)
        texto = Acuatico.desplazarse(self) + Terrestre.desplazarse(self)
        self.energia = nueva_energia
        return texto
    pass


if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2, cantidad_patas=6)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()
