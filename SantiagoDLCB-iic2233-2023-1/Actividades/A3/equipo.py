from collections import defaultdict, deque


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad

    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)

    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        # Completar
        if id_jugador in self.jugadores.keys():
            return False
        else:
            self.jugadores.update({id_jugador: jugador})
            return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        # Completar
        if id_jugador not in self.jugadores.keys():
            return -1
        else:
            largo_inicial = len(self.dict_adyacencia[id_jugador])
            for vecino in vecinos:
                self.dict_adyacencia[id_jugador].add(vecino)

            return len(self.dict_adyacencia[id_jugador]) - largo_inicial

    def mejor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad más similar.'''
        # Completar
        jugador = self.jugadores[id_jugador]
        amigos = self.dict_adyacencia[id_jugador]
        mejor_amigo = None
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        for id_amigo in amigos:
            amigo = self.jugadores[id_amigo]
            if mejor_amigo is None:
                mejor_amigo = amigo
            else:
                actual = abs(mejor_amigo.velocidad - jugador.velocidad)
                nuevo = abs(amigo.velocidad - jugador.velocidad)
                if actual > nuevo:
                    mejor_amigo = amigo
        return mejor_amigo

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        # Completar
        jugador = self.jugadores[id_jugador]
        peor_companero = None
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        for id in self.jugadores.keys():
            companero = self.jugadores[id]
            if peor_companero is None:
                peor_companero = companero
            else:
                actual = abs(peor_companero.velocidad - jugador.velocidad)
                nuevo = abs(companero.velocidad - jugador.velocidad)
                if nuevo > actual:
                    peor_companero = companero
        return peor_companero

    def peor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al amigo con la mayor diferencia de velocidad.'''
        # Completar
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        jugador = self.jugadores[id_jugador]
        visitados = set()
        cola = deque([id_jugador])

        while len(cola) > 0:
            id_actual = cola.popleft()
            visitados.add(id_actual)
            for id in self.dict_adyacencia[id_actual]:
                if id not in visitados and id not in cola:
                    cola.append(id)
        peor_conocido = None
        for id in visitados:
            conocido = self.jugadores[id]
            if peor_conocido is None:
                peor_conocido = conocido
            else:
                actual = abs(peor_conocido.velocidad - jugador.velocidad)
                nuevo = abs(conocido.velocidad - jugador.velocidad)
                if nuevo > actual:
                    peor_conocido = conocido
        return peor_conocido

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        visitados = set()
        cola = deque([id_jugador_1])
        distancias = {id_jugador_1: 0}

        id_actual = id_jugador_1
        while len(cola) > 0:
            id_actual = cola.popleft()
            visitados.add(id_actual)
            for id in self.dict_adyacencia[id_actual]:
                if id not in visitados and id not in cola:
                    cola.append(id)
                    if id not in distancias.keys():
                        nueva_distancia = distancias[id_actual]+1
                        distancias.update({id: nueva_distancia})
        if id_jugador_2 in distancias.keys():
            return distancias[id_jugador_2]
        return -1


if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)

    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}')
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
