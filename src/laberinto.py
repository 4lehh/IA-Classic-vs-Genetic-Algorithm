"""Módulo que define la clase Laberinto y su lógica de funcionamiento."""

from random import randint, random, sample

from casilla_laberinto import CasillaLaberinto
from jugador import Jugador, JugadorGenetico, JugadorGreedy, JugadorRandom
from movimientos import MovimientosPosibles
from tipo_jugador import TipoJugador


class Laberinto:
    """Clase que representa un laberinto con jugador, metas y murallas."""

    laberinto: list[list[CasillaLaberinto]]

    jugador: Jugador
    ticks_transcurridos: int

    dimenciones: tuple[int, int]
    prob_murallas: float
    prob_mover_murallas: float
    n_metas: int

    jugador_pos: tuple[int, int]
    metas_pos: list[tuple[int, int]]
    meta_real_pos: tuple[int, int]
    murallas_pos: list[tuple[int, int]]

    tipo_anterior_casilla_actual: CasillaLaberinto | None

    def __init__(
        self,
        dimenciones: tuple[int, int],
        prob_murallas: float = 0.2,
        prob_mover_murallas: float = 0.3,
        n_metas: int = 3,
        tipo_jugador: TipoJugador = TipoJugador.RANDOM,
    ):
        """Inicializa el laberinto con sus dimensiones y probabilidades.

        Args:
            dimenciones (tuple[int, int]): Dimensiones del laberinto.
            prob_murallas (float): Probabilidad de generacion de murallas.
            prob_mover_murallas (float): Probabilidad de mover cada muralla.
            n_metas (int): Número de metas en el laberinto.
        """

        match tipo_jugador:
            case TipoJugador.RANDOM:
                self.jugador = JugadorRandom(self)
            case TipoJugador.GREEDY:
                self.jugador = JugadorGreedy(self)
            case TipoJugador.GENETICO:
                self.jugador = JugadorGenetico(self)
            case _:
                raise ValueError(f"Tipo de jugador no reconocido: {tipo_jugador}")

        self.ticks_transcurridos = 0

        self.dimenciones = dimenciones
        self.prob_murallas = prob_murallas
        self.prob_mover_murallas = prob_mover_murallas

        self.murallas_pos = []

        self.n_metas = n_metas
        self.metas_pos = []

        self.tipo_anterior_casilla_actual = None

        try:
            self._crear_laberinto()
        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            raise

    def _crear_laberinto(self):
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
                self.meta_real_pos = (mx, my)
            else:
                self.laberinto[mx][my] = CasillaLaberinto.META_FALSA
            self.metas_pos.append((mx, my))

    def tick(self):
        """Mueve las murallas de forma aleatoria y ejecuta el tick del jugador."""
        self.mover_jugador()

        self.mover_murallas()

    def mover_murallas(self):
        """Mueve las murallas de forma aleatoria en el laberinto."""
        nuevas_murallas = set()
        filas, columnas = self.dimenciones

        for mx, my in self.murallas_pos:
            nueva_pos = (mx, my)
            if random() <= self.prob_mover_murallas:
                movimientos_muralla = [
                    m for m in MovimientosPosibles if m != MovimientosPosibles.NO_MOVERSE
                ]
                mov = movimientos_muralla[randint(0, len(movimientos_muralla) - 1)]
                dx, dy = mov.value
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

    def mover_jugador(self):
        """Mueve al jugador según su tick y actualiza su posición en el laberinto."""
        # Mover jugador usando su tick
        movimiento_jugador = self.jugador.tick()
        if movimiento_jugador == MovimientosPosibles.NO_MOVERSE:
            return

        # Calcular coordenadas nuevas
        dx, dy = movimiento_jugador.value
        x, y = self.jugador_pos
        nx, ny = x + dx, y + dy

        # Actualiza la casilla anterior
        if self.tipo_anterior_casilla_actual is None:
            self.laberinto[x][y] = CasillaLaberinto.CAMINO
        else:
            self.laberinto[x][y] = self.tipo_anterior_casilla_actual

        # Actualiza la posición del jugador
        self.tipo_anterior_casilla_actual = self.laberinto[nx][ny]
        self.jugador_pos = (nx, ny)
        self.laberinto[nx][ny] = CasillaLaberinto.JUGADOR

        self.ticks_transcurridos += 1

    def casillas_adyacentes(self, pos=None):
        """Devuelve un dict con los movimientos posibles y el tipo de casilla adyacente al jugador (o a la posición dada)."""
        if pos is None:
            x, y = self.jugador_pos
        else:
            x, y = pos

        adyacentes = {}
        for mov in MovimientosPosibles:
            dx, dy = mov.value
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.dimenciones[0] and 0 <= ny < self.dimenciones[1]:
                adyacentes[mov] = self.laberinto[nx][ny]
        return adyacentes

    def jugador_gano(self) -> bool:
        """
        Verifica si el jugador ha llegado a la meta real.

        Returns:
            bool: True si el jugador está en la meta real, False en caso contrario.
        """
        if self.jugador_pos == self.meta_real_pos:
            return True
        return False

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
        """Imprime el laberinto en formato markdown y muestra la leyenda de símbolos."""
        print(self._mostrar_markdown())
        print("\nLeyenda: 🧑=Jugador, 🏁=Meta real, ❌=Meta falsa, ⬛=Muralla, ⬜=Camino")
