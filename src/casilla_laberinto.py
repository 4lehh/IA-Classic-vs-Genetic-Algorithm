"""Módulo que define la clase CasillaLaberinto."""

from enum import Enum, auto


class CasillaLaberinto(Enum):
    """Representa los tipos de casillas en el laberinto."""

    MURALLA = auto()
    CAMINO = auto()
    JUGADOR = auto()
    META_FALSA = auto()
    META_REAL = auto()
