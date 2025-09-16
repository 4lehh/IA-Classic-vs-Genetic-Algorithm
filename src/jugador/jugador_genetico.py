from jugador import Jugador
from movimientos import MovimientosPosibles


class JugadorGenetico(Jugador):
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
