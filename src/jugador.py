"""Módulo que define la clase Jugador."""

from random import choice
from typing import TYPE_CHECKING, Callable, Optional

from casilla_laberinto import CasillaLaberinto
from movimientos import MovimientosPosibles

if TYPE_CHECKING:
    from laberinto import Laberinto


class Jugador:
    """Clase que representa al jugador en el laberinto."""

    laberinto: "Laberinto"

    def __init__(
        self,
        laberinto,
        estrategia_movimiento: Optional[
            Callable[[list[MovimientosPosibles]], MovimientosPosibles]
        ] = None,
    ):
        """
        Inicializa el jugador con referencia al laberinto y una estrategia de movimiento.

        Args:
            laberinto: Instancia del laberinto.
            estrategia_movimiento: Función que decide el siguiente movimiento. Debe recibir una lista de MovimientosPosibles y devolver un MovimientosPosibles.
        """
        self.laberinto = laberinto
        self.estrategia_movimiento = estrategia_movimiento or self._eleccion_movimiento_random

    def tick(self):
        """Elige y retorna un movimiento válido para el jugador usando la estrategia."""
        adyacentes = self.laberinto.casillas_adyacentes()
        movimientos_validos = [
            mov
            for mov, casilla in adyacentes.items()
            if casilla
            in [CasillaLaberinto.CAMINO, CasillaLaberinto.META_FALSA, CasillaLaberinto.META_REAL]
        ]
        return self.estrategia_movimiento(movimientos_validos)

    def _eleccion_movimiento_random(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """Elige uno de los movimientos validos de forma random."""
        movimiento_elegido = MovimientosPosibles.NO_MOVERSE
        if movimientos_validos:
            movimiento_elegido = choice(movimientos_validos)
        return movimiento_elegido
