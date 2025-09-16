"""Módulo que define el jugador greedy para el laberinto."""

from jugador import Jugador
from models import MovimientosPosibles


class JugadorGreedy(Jugador):
    """Jugador que utiliza una heurística greedy para decidir movimientos en el laberinto."""

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """
        Elige el movimiento más prometedor según una heurística (no implementado).

        Args:
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles para el jugador.

        Returns:
            MovimientosPosibles: Movimiento elegido por la heurística.
        """
        raise NotImplementedError("JugadorGreedy aun no esta implementado.")
