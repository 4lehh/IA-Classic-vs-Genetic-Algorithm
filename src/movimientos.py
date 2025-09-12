from enum import Enum


class MovimientosPosibles(Enum):
    ARRIBA = (-1, 0)
    ABAJO = (1, 0)
    IZQUIERDA = (0, -1)
    DERECHA = (0, 1)
    NO_MOVERSE = (0, 0)  # Solo lo usa el jugador
