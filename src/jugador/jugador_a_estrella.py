"""Módulo que define el jugador basado en el algoritmo A* para el laberinto."""

from collections import deque
from random import choice

from jugador import Jugador
from models import Coordenada, MovimientosPosibles


class JugadorAEstrella(Jugador):
    """
    Jugador que utiliza el algoritmo A* para encontrar la ruta óptima hacia la meta.

    La heurística utilizada es la distancia Manhattan.
    Además, se penalizan las posiciones recientemente visitadas para evitar ciclos y encontrar rutas más eficientes.
    """

    costo_acumulado: dict[Coordenada, int]
    visitados_recientes: deque[Coordenada]
    metas_visitadas: list[Coordenada]

    def __init__(self, laberinto):
        """Inicializa el jugador A* con referencias y estructuras internas."""
        super().__init__(laberinto)
        self.costo_acumulado = {}
        self.visitados_recientes = deque(maxlen=10)
        self.metas_visitadas = []

    def _eleccion_moverse(self, movimientos_validos):
        posicion_jugador = self.laberinto.jugador_pos
        g_actual = self._obtener_costo(posicion_jugador)
        posicion_meta = self._seleccionar_meta()
        mejor_mov = self._calcular_mejor_movimiento(
            posicion_jugador, movimientos_validos, g_actual, posicion_meta
        )
        self._actualizar_estado(posicion_jugador, mejor_mov, g_actual, posicion_meta)
        return mejor_mov

    def _seleccionar_meta(self) -> Coordenada:
        """
        Selecciona la meta no visitada más cercana al jugador (según distancia Manhattan).
        Si hay varias metas a la misma distancia mínima, selecciona una al azar entre ellas.

        Returns:
            Coordenada: Posición de la meta seleccionada.
        """

        return choice(
            self.laberinto.metas_mas_cercanas_a_posicion(
                self.laberinto.jugador_pos, self.metas_visitadas
            )
        )

    def _obtener_costo(self, posicion_jugador: Coordenada) -> int:
        """
        Obtiene el costo acumulado para la posición dada.

        Args:
            posicion_jugador (Coordenada): Posición del jugador.

        Returns:
            int: Costo acumulado.
        """
        return self.costo_acumulado.get(posicion_jugador, 0)

    def _costo_funcion_f(
        self, g_nuevo: int, nueva_posicion: Coordenada, posicion_meta: Coordenada
    ) -> int:
        """
        Calcula la función de costo F = G + H para el algoritmo A*.

        Args:
            g_nuevo (int): Costo acumulado hasta la nueva posición.
            nueva_posicion (Coordenada): Nueva posición tras el movimiento.
            posicion_meta (Coordenada): Posición de la meta objetivo.

        Returns:
            int: Valor de la función F para la nueva posición.
        """
        h = posicion_meta.distancia_manhatan(nueva_posicion)
        return g_nuevo + h

    def _calcular_mejor_movimiento(
        self,
        posicion_jugador: Coordenada,
        movimientos_validos: list[MovimientosPosibles],
        g_actual: int,
        posicion_meta: Coordenada,
    ):
        """
        Calcula el mejor movimiento posible según la función de costo F.

        Args:
            posicion_jugador (Coordenada): Posición actual del jugador.
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles.
            g_actual (int): Costo acumulado actual.
            posicion_meta (Coordenada): Meta objetivo.

        Returns:
            MovimientosPosibles: Mejor movimiento según la función F.
        """
        # Recordar: F = G + H donde G es el costo acumulado y H es la heurística (distancia a la meta usando distancia Manhattan)
        mejor_mov = None
        mejor_f = float("inf")

        # Recorremos los movimientos validos y calculamos su F
        for mov in movimientos_validos:
            # Posicion nueva si se realiza el movimiento
            nueva_pos = posicion_jugador + mov
            resultado_funcion_f = self._costo_funcion_f(g_actual + 1, nueva_pos, posicion_meta)

            # Penalizacion por repeticion de posiciones recientes (¿Razón? tiende a caer en bucles antonio)
            if nueva_pos in self.visitados_recientes:
                resultado_funcion_f += 5

            # Elegir al mejor F
            if resultado_funcion_f < mejor_f:
                mejor_f = resultado_funcion_f
                mejor_mov = mov

        # Puede que no haya un movimiento válido
        if mejor_mov is None:
            return choice(movimientos_validos)
        return mejor_mov

    def _actualizar_estado(self, posicion_jugador, mov, g_actual, posicion_meta):
        """
        Actualiza el estado interno del jugador tras realizar un movimiento.

        Args:
            posicion_jugador (Coordenada): Posición actual.
            mov (MovimientosPosibles): Movimiento realizado.
            g_actual (int): Costo acumulado actual.
            posicion_meta (Coordenada): Meta objetivo.
        """
        nueva_posicion = posicion_jugador + mov

        # Guardamos ultimas posiciones para evitar ciclos
        self.visitados_recientes.append(nueva_posicion)

        # Actualizo el costo acumulado para la nueva posicion
        self.costo_acumulado[nueva_posicion] = g_actual + 1

        # Si llegué a una meta la marco para no luego no tratar de ir hacia ella
        if posicion_meta == nueva_posicion:
            self.metas_visitadas.append(posicion_meta)
