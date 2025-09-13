"""Módulo que define la clase Jugador."""

from abc import abstractmethod
from random import choice
from typing import TYPE_CHECKING, Callable, Optional

from casilla_laberinto import CasillaLaberinto
from movimientos import MovimientosPosibles

if TYPE_CHECKING:
    from laberinto import Laberinto


@abstractmethod
class Jugador:
    """Clase que representa al jugador en el laberinto."""

    laberinto: "Laberinto"

    def __init__(
        self,
        laberinto,
    ):
        """
        Inicializa el jugador con referencia al laberinto.

        Args:
            laberinto: Instancia del laberinto.
        """
        self.laberinto = laberinto

    def tick(self) -> MovimientosPosibles:
        """Elige y retorna un movimiento válido para el jugador."""
        adyacentes = self.laberinto.casillas_adyacentes()

        movimientos_validos = [
            mov
            for mov, casilla in adyacentes.items()
            if casilla
            in [CasillaLaberinto.CAMINO, CasillaLaberinto.META_FALSA, CasillaLaberinto.META_REAL]
        ]

        if not movimientos_validos:
            return MovimientosPosibles.NO_MOVERSE

        return self._eleccion_moverse(movimientos_validos)

    @abstractmethod
    def _eleccion_moverse(
        self,
        movimientos_validos: list[MovimientosPosibles],
    ) -> MovimientosPosibles:
        """Método abstracto que debe ser implementado por las subclases."""
        pass


class JugadorRandom(Jugador):
    """Clase que representa un jugador que se mueve de forma aleatoria."""

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """Elige un movimiento aleatorio entre los movimientos válidos."""

        return choice(movimientos_validos)


class JugadorGreedy(Jugador):
    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        pass


class JugadorGenetico(Jugador):
    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        pass
