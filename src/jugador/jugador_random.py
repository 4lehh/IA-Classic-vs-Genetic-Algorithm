from random import choice

from jugador import Jugador
from movimientos import MovimientosPosibles


class JugadorRandom(Jugador):
    """Clase que representa un jugador que se mueve de forma aleatoria."""

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """
        Elige un movimiento aleatorio entre los movimientos válidos.

        Args:
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles para el jugador.

        Returns:
            MovimientosPosibles: Movimiento elegido aleatoriamente.
        """
        return choice(movimientos_validos)
