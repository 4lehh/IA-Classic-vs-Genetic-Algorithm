from jugador import Jugador
from movimientos import MovimientosPosibles


class JugadorGreedy(Jugador):
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
