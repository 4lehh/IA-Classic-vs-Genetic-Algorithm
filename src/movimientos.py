"""Módulo que define los movimientos posibles en el laberinto."""

from enum import Enum


class MovimientosPosibles(Enum):
    """Enumera los movimientos posibles para el jugador y murallas."""

    ARRIBA = (-1, 0)
    ABAJO = (1, 0)
    IZQUIERDA = (0, -1)
    DERECHA = (0, 1)
    NO_MOVERSE = (0, 0)  # Solo lo usa el jugador
