"""Módulo que define el jugador greedy para el laberinto."""

from random import choice

from exceptions import MetaNoEncontradaError
from jugador import Jugador
from models import CasillaLaberinto, Coordenada, MovimientosPosibles


class JugadorGreedy(Jugador):
    """
    Jugador que utiliza una heurística greedy para decidir movimientos en el laberinto.

    Selecciona el movimiento que minimiza la distancia Manhattan a la meta más cercana.
    """

    metas_visitadas: list[Coordenada]
    meta_objetivo: Coordenada | None

    def __init__(self, laberinto):
        """Inicializa el jugador greedy y su lista de metas visitadas."""
        super().__init__(laberinto)
        self.metas_visitadas = []
        self.meta_objetivo = None

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """
        Elige el movimiento que minimiza la distancia Manhattan a la meta más cercana.

        Args:
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles para el jugador.

        Returns:
            MovimientosPosibles: Movimiento elegido por la heurística greedy.
        """
        if self.meta_objetivo is None:
            self.meta_objetivo = self._meta_mas_cercana()

        pos_actual = self.laberinto.jugador_pos

        distancia_actual = pos_actual.distancia_manhatan(self.meta_objetivo)
        mejor_movimiento = []
        mejor_distancia = distancia_actual

        for mov in movimientos_validos:
            nueva_distancia = (pos_actual + mov).distancia_manhatan(self.meta_objetivo)
            if nueva_distancia < mejor_distancia:
                mejor_distancia = nueva_distancia
                mejor_movimiento = [mov]
            elif nueva_distancia == mejor_distancia and mejor_distancia < distancia_actual:
                mejor_movimiento.append(mov)

        movimiento_elegido = MovimientosPosibles.NO_MOVERSE
        if mejor_movimiento:
            movimiento_elegido = choice(mejor_movimiento)

        pos_futura = pos_actual + movimiento_elegido
        if self.laberinto.laberinto[pos_futura.x][pos_futura.y] == CasillaLaberinto.META_FALSA:
            self.metas_visitadas.append(pos_futura)
            self.meta_objetivo = None

        return movimiento_elegido

    def _meta_mas_cercana(self) -> Coordenada:
        """
        Encuentra la(s) meta(s) más cercana(s) al jugador según la distancia Manhattan.

        Returns:
            Coordenada: Una de las metas más cercanas (aleatoria si hay empate).

        Raises:
            MetaNoEncontradaError: Si no hay metas disponibles para dirigirse.
        """
        metas_mas_cercanas = []
        pos_actual = self.laberinto.jugador_pos
        distancia_minima_encontrada = float("inf")

        for meta in self.laberinto.metas_pos:
            if meta in self.metas_visitadas:
                continue

            distancia_a_la_meta = pos_actual.distancia_manhatan(meta)

            if distancia_a_la_meta < distancia_minima_encontrada:
                distancia_minima_encontrada = distancia_a_la_meta
                metas_mas_cercanas = [meta]
            elif distancia_a_la_meta == distancia_minima_encontrada:
                metas_mas_cercanas.append(meta)

        if not metas_mas_cercanas:
            raise MetaNoEncontradaError("No hay metas a la cual dirigirse.")

        return choice(metas_mas_cercanas)
