"""Módulo que define la clase Laberinto y su lógica de funcionamiento."""

from random import randint, random, sample
from typing import Optional, Type

from exceptions import CreacionLaberintoError, MovimientoInvalidoError
from jugador import Jugador, JugadorRandom
from models import CasillaLaberinto, Coordenada, MovimientosPosibles


class Laberinto:
    """Clase que representa un laberinto con jugador, metas y murallas."""

    laberinto: list[list[CasillaLaberinto]]

    jugador: Jugador
    ticks_transcurridos: int

    filas: int
    columnas: int
    prob_murallas: float
    prob_mover_murallas: float
    n_metas: int

    jugador_pos: Coordenada
    metas_pos: list[Coordenada]
    meta_real_pos: Coordenada
    murallas_pos: list[Coordenada]

    tipo_anterior_casilla_actual: CasillaLaberinto | None

    def __init__(
        self,
        dimensiones: tuple[int, int],
        prob_murallas: float = 0.2,
        prob_mover_murallas: float = 0.3,
        n_metas: int = 3,
        clase_jugador: Type[Jugador] = JugadorRandom,
        jugar_instanciado: Optional[Jugador] = None,
    ):
        """
        Inicializa el laberinto con sus dimensiones y probabilidades.

        Args:
            dimensiones (tuple[int, int]): Dimensiones del laberinto.
            prob_murallas (float): Probabilidad de generación de murallas.
            prob_mover_murallas (float): Probabilidad de mover cada muralla.
            n_metas (int): Número de metas en el laberinto.
            clase_jugador (Type[Jugador]): Clase del jugador a instanciar.
        """
        self.filas, self.columnas = dimensiones
        self.prob_murallas = prob_murallas
        self.prob_mover_murallas = prob_mover_murallas

        self.murallas_pos = []

        self.n_metas = n_metas
        self.metas_pos = []

        self.tipo_anterior_casilla_actual = None

        if jugar_instanciado is not None:
            self.jugador = jugar_instanciado
        else:
            self.jugador = clase_jugador(self)

        self.ticks_transcurridos = 0

        try:
            self._crear_laberinto()
        except Exception as e:
            print(f"Error al crear el laberinto: {e}")
            raise

        if jugar_instanciado is None:
            print(f"Laberinto creado con Jugador de Tipo {self.jugador.__class__.__name__}.")

    def _crear_laberinto(self):
        self.laberinto = []
        caminos_libres = []

        # Crear el laberinto aleatorio
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                coordenada = Coordenada(i, j)
                if random() <= self.prob_murallas:
                    fila.append(CasillaLaberinto.MURALLA)
                    self.murallas_pos.append(coordenada)
                else:
                    fila.append(CasillaLaberinto.CAMINO)
                    caminos_libres.append(coordenada)
            self.laberinto.append(fila)

        # Seleccionar posición inicial del jugador
        if not caminos_libres:
            raise CreacionLaberintoError(
                "No hay caminos libres para ubicar al jugador. El laberinto generado es inválido."
            )

        self.jugador_pos = caminos_libres.pop(randint(0, len(caminos_libres) - 1))
        self.laberinto[self.jugador_pos.x][self.jugador_pos.y] = CasillaLaberinto.JUGADOR

        # Seleccionar posiciones de metas
        if len(caminos_libres) < self.n_metas:
            raise CreacionLaberintoError(
                f"No hay suficientes caminos libres para ubicar las metas. Se requieren {self.n_metas}, pero solo hay {len(caminos_libres)} disponibles."
            )

        # Elige de forma aleatoria las n metas (Real y falsas)
        metas = sample(caminos_libres, self.n_metas)
        real_id = randint(0, self.n_metas - 1)

        for id, meta in enumerate(metas):
            if id == real_id:
                self.laberinto[meta.x][meta.y] = CasillaLaberinto.META_REAL
                self.meta_real_pos = meta
            else:
                self.laberinto[meta.x][meta.y] = CasillaLaberinto.META_FALSA
            self.metas_pos.append(meta)

    def coordenada_en_laberinto(self, coordenada: Coordenada) -> bool:
        """Verifica si una coordenada está dentro de los límites del laberinto."""
        if 0 <= coordenada.x < self.filas and 0 <= coordenada.y < self.columnas:
            return True
        return False

    def tick(self):
        """Mueve las murallas de forma aleatoria y ejecuta el tick del jugador."""
        self.mover_jugador()

        self.mover_murallas()

    def mover_murallas(self):
        """Mueve las murallas de forma aleatoria en el laberinto."""
        nuevas_murallas: set[Coordenada] = set()

        for muralla in self.murallas_pos:
            nueva_pos = muralla
            if random() <= self.prob_mover_murallas:
                movimientos_muralla = [
                    m for m in MovimientosPosibles if m != MovimientosPosibles.NO_MOVERSE
                ]
                mov = movimientos_muralla[randint(0, len(movimientos_muralla) - 1)]
                nueva_posicion = muralla + mov
                # Verifica que la nueva posición esté dentro del laberinto y no colisione

                if (
                    self.coordenada_en_laberinto(nueva_posicion)
                    and self.laberinto[nueva_posicion.x][nueva_posicion.y]
                    == CasillaLaberinto.CAMINO
                    and nueva_posicion not in nuevas_murallas
                ):
                    # Actualiza la casilla anterior a CAMINO
                    self.laberinto[muralla.x][muralla.y] = CasillaLaberinto.CAMINO
                    # Mueve la muralla
                    self.laberinto[nueva_posicion.x][nueva_posicion.y] = CasillaLaberinto.MURALLA
                    nueva_pos = nueva_posicion
            nuevas_murallas.add(nueva_pos)
        self.murallas_pos = list(nuevas_murallas)

    def mover_jugador(self):
        """Mueve al jugador según su tick y actualiza su posición en el laberinto."""
        self.ticks_transcurridos += 1

        # Mover jugador usando su tick
        movimiento_jugador = self.jugador.tick()
        if movimiento_jugador == MovimientosPosibles.NO_MOVERSE:
            return

        # Calcular coordenadas nuevas
        nueva_posicion = self.jugador_pos + movimiento_jugador

        if not self.coordenada_en_laberinto(nueva_posicion):
            raise MovimientoInvalidoError(
                f"El movimiento elegido por el jugador lo saca del mapa. Esto indica un error en la lógica de movimientos posibles.\n"
                f"Posición actual: {self.jugador_pos}.\n"
                f"Movimiento elegido: {movimiento_jugador}.\n"
                f"Nueva posición calculada: {nueva_posicion}.\n"
                f"Dimensiones del laberinto: {self.filas}x{self.columnas}."
            )

        # Actualiza la casilla anterior
        if self.tipo_anterior_casilla_actual is None:
            self.laberinto[self.jugador_pos.x][self.jugador_pos.y] = CasillaLaberinto.CAMINO
        else:
            self.laberinto[self.jugador_pos.x][
                self.jugador_pos.y
            ] = self.tipo_anterior_casilla_actual

        # Actualiza la posición del jugador
        self.tipo_anterior_casilla_actual = self.laberinto[nueva_posicion.x][nueva_posicion.y]
        self.jugador_pos = nueva_posicion
        self.laberinto[nueva_posicion.x][nueva_posicion.y] = CasillaLaberinto.JUGADOR

    def casillas_adyacentes(
        self, posicion: Optional[Coordenada] = None
    ) -> dict[MovimientosPosibles, Coordenada]:
        """Devuelve un dict con los movimientos posibles y el tipo de casilla adyacente al jugador (o a la posición dada)."""
        if posicion is None:
            posicion = self.jugador_pos

        adyacentes = {}
        for mov in MovimientosPosibles:
            nueva_posicion = posicion + mov
            if self.coordenada_en_laberinto(nueva_posicion):
                adyacentes[mov] = self.laberinto[nueva_posicion.x][nueva_posicion.y]
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

    def imprimir(self):
        """Imprime el laberinto en formato markdown y muestra la leyenda de símbolos de forma dinámica."""
        filas_md = []
        for fila in self.laberinto:
            filas_md.append("".join(c.value for c in fila))
        print("\n".join(filas_md))

        leyenda = "\nLeyenda: " + ", ".join(
            f"{casilla.value}={casilla.name.replace('_', ' ').capitalize()}"
            for casilla in CasillaLaberinto
        )
        print(leyenda)
