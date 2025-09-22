"""Módulo que define la clase Jugador."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from models import CasillaLaberinto, MovimientosPosibles

if TYPE_CHECKING:
    from laberinto import Laberinto


class Jugador(ABC):
    """Clase que representa al jugador en el laberinto."""

    laberinto: "Laberinto"
    cantidad_tick: int = 0

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
        """
        Calcula y retorna el movimiento que debe realizar el jugador en el laberinto.

        Returns:
            MovimientosPosibles: Movimiento elegido por el jugador.
        """
        adyacentes = self.laberinto.casillas_adyacentes()

        movimientos_validos = [
            mov
            for mov, casilla in adyacentes.items()
            if casilla
            in [CasillaLaberinto.CAMINO, CasillaLaberinto.META_FALSA, CasillaLaberinto.META_REAL]
        ]

        if not movimientos_validos:
            return MovimientosPosibles.NO_MOVERSE

        self.cantidad_tick += 1
        return self._eleccion_moverse(movimientos_validos)

    @abstractmethod
    def _eleccion_moverse(
        self,
        movimientos_validos: list[MovimientosPosibles],
    ) -> MovimientosPosibles:
        """Método abstracto que debe ser implementado por las subclases."""
        pass
