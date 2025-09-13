from enum import Enum, auto


class TipoJugador(Enum):
    """Enumera los tipos de jugadores disponibles."""

    RANDOM = auto()
    GREEDY = auto()
    GENETICO = auto()
