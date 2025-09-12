"""Módulo que define la clase Jugador."""

from random import choice
from typing import TYPE_CHECKING

from casilla_laberinto import CasillaLaberinto
from movimientos import MovimientosPosibles

if TYPE_CHECKING:
    from laberinto import Laberinto


class Jugador:
    """Clase que representa al jugador en el laberinto."""

    laberinto: "Laberinto"

    def __init__(self, laberinto: "Laberinto"):
        """Inicializa el jugador con referencia al laberinto."""
        self.laberinto = laberinto

    def tick(self):
        """
        Elige y retorna un movimiento válido para el jugador.

        La lógica de decisión está delegada a una función interna,
        permitiendo modificar fácilmente la estrategia de movimiento
        (por ejemplo, aleatoria, heurística, IA, etc.) sin cambiar la interfaz pública.
        """
        adyacentes = self.laberinto.casillas_adyacentes()
        movimientos_validos = [
            mov
            for mov, casilla in adyacentes.items()
            if casilla
            in [
                CasillaLaberinto.CAMINO,
                CasillaLaberinto.META_FALSA,
                CasillaLaberinto.META_REAL,
            ]
        ]
        return self._eleccion_movimiento_random(movimientos_validos)

    def _eleccion_movimiento_random(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """Elige uno de los movimientos validos de forma random."""
        movimiento_elegido = MovimientosPosibles.NO_MOVERSE
        if movimientos_validos:
            movimiento_elegido = choice(movimientos_validos)
        return movimiento_elegido
