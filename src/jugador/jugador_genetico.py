"""Módulo que define el jugador basado en algoritmo genético para el laberinto."""

from jugador import Jugador
from models import MovimientosPosibles


class JugadorGenetico(Jugador):
    """Jugador que utiliza un algoritmo genético para decidir movimientos en el laberinto."""

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """
        Elige el movimiento usando un algoritmo genético (no implementado).

        Args:
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles para el jugador.

        Returns:
            MovimientosPosibles: Movimiento elegido por el algoritmo genético.
        """
        raise NotImplementedError("JugadorGenetico aun no esta implementado.")
