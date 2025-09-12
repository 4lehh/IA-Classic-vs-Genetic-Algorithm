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
    prob_mover_murallas: float
    n_metas: int

    jugador_pos: tuple[int, int]
    metas_pos: list[tuple[int, int]]
    murallas_pos: list[tuple[int, int]]

    def __init__(
        self,
        dimenciones: tuple[int, int],
        prob_murallas: float = 0.2,
        prob_mover_murallas: float = 0.3,
        n_metas: int = 3,
    ):
        self.dimenciones = dimenciones
        self.prob_murallas = prob_murallas
        self.prob_mover_murallas = prob_mover_murallas

        self.murallas_pos = []

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
                    self.murallas_pos.append((i, j))
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

    def tick(self):
        """Mueve las murallas de forma aleatoria"""
        movimientos_validos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        nuevas_murallas = set()
        filas, columnas = self.dimenciones

        for id, (mx, my) in enumerate(self.murallas_pos):
            nueva_pos = (mx, my)
            if random() <= self.prob_mover_murallas:
                dx, dy = movimientos_validos[randint(0, 3)]
                nx, ny = mx + dx, my + dy

                # Verifica que la nueva posición esté dentro del laberinto y no colisione
                if (
                    0 <= nx < filas
                    and 0 <= ny < columnas
                    and self.laberinto[nx][ny] == CasillaLaberinto.CAMINO
                    and (nx, ny) not in nuevas_murallas
                ):
                    # Actualiza la casilla anterior a CAMINO
                    self.laberinto[mx][my] = CasillaLaberinto.CAMINO

                    # Mueve la muralla
                    self.laberinto[nx][ny] = CasillaLaberinto.MURALLA

                    nueva_pos = (nx, ny)

            nuevas_murallas.add(nueva_pos)
        self.murallas_pos = list(nuevas_murallas)

    def _mostrar_markdown(self) -> str:
        """Devuelve una representación del laberinto en formato markdown."""
        simbolos = {
            CasillaLaberinto.MURALLA: "⬛",
            CasillaLaberinto.CAMINO: "⬜",
            CasillaLaberinto.JUGADOR: "🧑",
            CasillaLaberinto.META_FALSA: "❌",
            CasillaLaberinto.META_REAL: "🏁",
        }
        filas_md = []
        for fila in self.laberinto:
            filas_md.append("".join(simbolos[c] for c in fila))
        return "\n".join(filas_md)

    def imprimir(self):
        print(self._mostrar_markdown())
        print("\nLeyenda: 🧑=Jugador, 🏁=Meta real, ❌=Meta falsa, ⬛=Muralla, ⬜=Camino")
