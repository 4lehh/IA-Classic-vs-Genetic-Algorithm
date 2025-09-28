"""Módulo que define el jugador basado en algoritmo genético para el laberinto."""

from collections import deque
from random import choice, random, uniform
from statistics import stdev
from typing import Optional

from exceptions import MetaNoEncontradaError
from jugador import Jugador
from jugador.jugador_q_learning_adaptado import JugadorQlearningAdaptado
from models import CasillaLaberinto, Coordenada, MovimientosPosibles


class JugadorGenetico(JugadorQlearningAdaptado):
    """
    Jugador que utiliza un algoritmo genético para decidir movimientos en el laberinto.

    Hereda de JugadorQlearningAdaptado y optimiza sus parámetros mediante generaciones.
    """

    lista_generaciones: list[JugadorQlearningAdaptado] | None

    def __init__(self, laberinto):
        """
        Inicializa el jugador genético.

        Args:
            laberinto: Instancia del laberinto donde el jugador se moverá.
        """
        Jugador.__init__(self, laberinto)
        self.lista_generaciones = None
        self._generaciones()

        self.Q = {}
        self.metas_visitadas = []
        self.posiciones_visitadas = deque(maxlen=10)

        self._inicializar_Q_table()
        self._entrenar(1000)
        self.mostrar_mapas_calor_Q()

    def _generaciones(
        self,
        cantidad_generaciones: int = 100,
        tamaño_poblacion: int = 100,
        max_steps: Optional[int] = None,
    ):
        """
        Genera una lista de generaciones de jugadores Q-Learning Estrella Adaptado.

        Args:
            cantidad_generaciones: Número de generaciones a crear.
            tamaño_poblacion: Número de individuos en cada generación.
        """
        from laberinto import Laberinto

        pasos_maximos = (
            (self.laberinto.filas + self.laberinto.columnas) * 10
            if max_steps is None
            else max_steps
        )

        for gen_num in range(cantidad_generaciones):
            if self.lista_generaciones is None:
                aux_gamma = random()
                aux_betha = random()
                self.lista_generaciones = [
                    JugadorQlearningAdaptado(
                        laberinto=self.laberinto,
                        alpha=1 - aux_gamma,
                        gamma=aux_gamma,
                        betha=aux_betha,
                        omega=1 - aux_betha,
                        epsilon=uniform(0.1, 0.4),
                    )
                    for _ in range(tamaño_poblacion)
                ]
            else:
                self.lista_generaciones = sorted(self.lista_generaciones, reverse=True)
                mejor_jugador = self.lista_generaciones[0]
                segundo_mejor_jugador = self.lista_generaciones[1]
                self._crossover_and_mutation(mejor_jugador, segundo_mejor_jugador)

            for jugador in self.lista_generaciones:
                jugador.cantidad_tick = 0
                jugador.posicion_inicial = jugador.laberinto.jugador_pos
                jugador.metas_visitadas = []
                jugador.posiciones_visitadas.clear()

                jugador.laberinto = Laberinto(
                    dimensiones=(self.laberinto.filas, self.laberinto.columnas),
                    prob_murallas=self.laberinto.prob_murallas,
                    prob_mover_murallas=self.laberinto.prob_mover_murallas,
                    n_metas=self.laberinto.n_metas,
                    clase_jugador=JugadorQlearningAdaptado,
                    jugar_instanciado=jugador,
                )
                for _ in range(pasos_maximos):
                    jugador.laberinto.tick()
                    if jugador.laberinto.jugador_gano():
                        break
                jugador.cantidad_tick = max(1, jugador.cantidad_tick)

        if self.lista_generaciones is None:
            raise ValueError("No hay jugadores en la lista de generaciones.")

        mejor = max(self.lista_generaciones)
        self.gamma = mejor.gamma
        self.alpha = mejor.alpha
        self.betha = mejor.betha
        self.omega = mejor.omega
        self.epsilon = uniform(0.1, 0.3)
        self.posiciones_visitadas = deque(maxlen=10)
        self.posicion_inicial = None

    def _crossover_and_mutation(
        self,
        mejor_jugador: JugadorQlearningAdaptado,
        segundo_mejor_jugador: JugadorQlearningAdaptado,
    ):
        """Realiza el cruce y la mutación de los jugadores seleccionados para formar una nueva generación."""
        if self.lista_generaciones is None:
            raise ValueError("No hay jugadores en la lista de generaciones.")

        for jugador in self.lista_generaciones[2:]:

            def cruzar_valor(v1, v2, min_val=0.0, max_val=1.0):
                media = (v1 + v2) / 2
                delta = abs(v1 - v2) / 2
                nuevo = uniform(media - delta, media + delta)
                return max(min_val, min(max_val, nuevo))  # Mantener dentro de rango

            jugador.gamma = cruzar_valor(mejor_jugador.gamma, segundo_mejor_jugador.gamma)
            jugador.alpha = 1 - jugador.gamma
            jugador.betha = cruzar_valor(mejor_jugador.betha, segundo_mejor_jugador.betha)
            jugador.omega = 1 - jugador.betha
            jugador.Q = {}

            # Mutación aleatoria con baja probabilidad (8%)
            if random() < 0.08:
                jugador.gamma = random()
                jugador.alpha = 1 - jugador.gamma

            if random() < 0.08:
                jugador.betha = random()
                jugador.omega = 1 - jugador.betha

            # Reiniciar Q-table y variables
            jugador._inicializar_Q_table()
            jugador.metas_visitadas = []
            jugador.posiciones_visitadas.clear()

    def _inicializar_Q_table(self):
        """Inicializa la Q-table para todas las posiciones posibles del laberinto."""
        for i in range(self.laberinto.filas):
            for j in range(self.laberinto.columnas):
                self.Q[Coordenada(i, j)] = {mov: 0.0 for mov in MovimientosPosibles}
