"""Módulo que define la clase CasillaLaberinto."""

from enum import Enum, auto


class CasillaLaberinto(Enum):
    """Representa los tipos de casillas en el laberinto."""

    MURALLA = "⬛"
    CAMINO = "⬜"
    JUGADOR = "🧑"
    META_FALSA = "❌"
    META_REAL = "🏁"
