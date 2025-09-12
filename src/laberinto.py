from enum import Enum, auto
from random import randint, random, sample


class CasillaLaberinto(Enum):
    MURALLA = auto()
    CAMINO = auto()
    JUGADOR = auto()
    META_FALSA = auto()
    META_REAL = auto()


class Laberinto:
    laberinto: list[list[CasillaLaberinto]]

    dimenciones: tuple[int, int]
    prob_murallas: float
    n_metas: int

    jugador_pos: tuple[int, int]
    metas_pos: list[tuple[int, int]]

    def __init__(self, dimenciones: tuple[int, int], prob_murallas: float = 0.2, n_metas: int = 3):
        self.dimenciones = dimenciones
        self.prob_murallas = prob_murallas
        self.n_metas = n_metas
        self.metas_pos = []

        try:
            self._crear_leberinto()
        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            raise

    def _crear_leberinto(self):
        filas, columnas = self.dimenciones
        self.laberinto = []
        caminos_libres = []

        # Crear el laberinto aleatorio
        for i in range(filas):
            fila = []
            for j in range(columnas):
                if random() <= self.prob_murallas:
                    fila.append(CasillaLaberinto.MURALLA)
                else:
                    fila.append(CasillaLaberinto.CAMINO)
                    caminos_libres.append((i, j))
            self.laberinto.append(fila)

        # Seleccionar posición inicial del jugador
        if not caminos_libres:
            raise ValueError("No hay caminos libres para ubicar al jugador.")

        self.jugador_pos = caminos_libres.pop(randint(0, len(caminos_libres) - 1))
        x, y = self.jugador_pos
        self.laberinto[x][y] = CasillaLaberinto.JUGADOR

        # Seleccionar posiciones de metas
        if len(caminos_libres) < self.n_metas:
            raise ValueError("No hay suficientes caminos libres para ubicar las metas.")

        # Elige de forma aleatoria las n metas (Real y falsas)
        metas = sample(caminos_libres, self.n_metas)
        real_id = randint(0, self.n_metas - 1)

        for id, (mx, my) in enumerate(metas):
            if id == real_id:
                self.laberinto[mx][my] = CasillaLaberinto.META_REAL
            else:
                self.laberinto[mx][my] = CasillaLaberinto.META_FALSA
            self.metas_pos.append((mx, my))
