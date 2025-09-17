"""
Módulo que implementa un jugador para laberintos combinando Q-learning y A*.

Este módulo define una clase que fusiona el aprendizaje por refuerzo (Q-learning) con la búsqueda informada de A*.
"""

from collections import deque
from random import choice, random
from typing import Optional

from exceptions import MetaNoEncontradaError
from jugador import Jugador
from models import CasillaLaberinto, Coordenada, MovimientosPosibles


class JugadorQlearningEstrella(Jugador):
    """
    Jugador que combina Q-learning y A* para aprender a moverse en el laberinto.

    Esta clase fusiona la exploración y aprendizaje de Q-learning con la heurística de búsqueda
    informada de A* (A estrella), utilizando recompensas tanto por acercarse a metas como por
    alcanzar la meta real, y ponderando la distancia heurística en la toma de decisiones.
    """

    alpha: float  # tasa de aprendizaje
    gamma: float  # descuento futuro
    epsilon: float  # Nivel de exploración
    Q: dict[
        Coordenada, dict[MovimientosPosibles, float]
    ]  # Tabla que representa, por cada posicion, que acciones podemos tomar, y por cada una de estas, cual es el valor que nos aporta tomar dicha accion
    metas_visitadas: list[Coordenada]
    posiciones_visitadas: deque[Coordenada]

    def __init__(self, laberinto, alpha=0.1, gamma=0.9, epsilon=0.2, betha=0.5, omega=0.5):
        """
        Inicializa una instancia de JugadorQlearningEstrella.

        Args:
            laberinto: Instancia del laberinto sobre el que se juega.
            alpha (float): Tasa de aprendizaje.
            gamma (float): Factor de descuento futuro.
            epsilon (float): Nivel de exploración.
            betha (float): Peso de la Q-table.
            omega (float): Peso de la heurística (distancia a la meta).
        """
        super().__init__(laberinto)
        self.alpha = alpha
        self.gamma = gamma
        self.betha = betha  # Peso de la Q-table
        self.omega = omega  # Peso de la heurística (distancia a la meta)
        self.epsilon = epsilon
        self.Q = {}
        self.metas_visitadas = []
        self.posiciones_visitadas = deque(maxlen=10)

        # Inicializar Q-table para cada posición posible
        for i in range(self.laberinto.filas):
            for j in range(self.laberinto.columnas):
                self.Q[Coordenada(i, j)] = {mov: 0.0 for mov in MovimientosPosibles}

        self._entrenar()
        self.mostrar_mapas_calor_Q()

    def _eleccion_moverse(self, movimientos_validos) -> MovimientosPosibles:
        """
        Elige el movimiento usando la política Q-learning entrenada.

        Args:
            movimientos_validos (list[MovimientosPosibles]): Movimientos posibles para el jugador.

        Returns:
            MovimientosPosibles: Movimiento elegido por la política Q-learning.
        """
        pos_actual = self.laberinto.jugador_pos
        # Variables auxiliares para la selección del mejor movimiento
        mejor_mov = None
        mejor_balance = 0.0
        metas_disponibles = [
            pos for pos in self.laberinto.metas_pos if pos not in self.metas_visitadas
        ]

        # Explorar o explotar
        if random() < self.epsilon:
            mejor_mov = choice(movimientos_validos)
        else:
            q_vals = {mov: self.Q[pos_actual][mov] for mov in movimientos_validos}
            for valores_coordenadas, costo_q_table in q_vals.items():
                meta = choice(metas_disponibles)

                # Idea: balance = betha*valor_que_aporta_la_accion_q_table - omega*distancia_euclidiana_a_la_meta

                balance = self.betha * costo_q_table - self.omega * meta.distancia_euclidiana(
                    pos_actual + valores_coordenadas
                )
                if balance > mejor_balance or mejor_mov is None:
                    mejor_balance = balance
                    mejor_mov = valores_coordenadas

            # Por si no elige nada
            if mejor_mov is None:
                return MovimientosPosibles.NO_MOVERSE

        # Simular nueva posición
        nueva_posicion = pos_actual + mejor_mov

        if not self.laberinto.coordenada_en_laberinto(nueva_posicion):
            return MovimientosPosibles.NO_MOVERSE

        casilla_siguiente = self.laberinto.laberinto[nueva_posicion.x][nueva_posicion.y]

        # Calcular recompensa
        reward = self._calcular_recompensa(pos_actual, nueva_posicion, casilla_siguiente)

        # Actualizar Q-table
        q_actual = self.Q[pos_actual][mejor_mov]
        q_max_sig = max(self.Q[nueva_posicion].values())

        # Actualiza el valor Q para la posición y acción actual usando la ecuación de Q-learning:
        # Q(s,a) ← Q(s,a) + α * [recompensa + γ * max(Q(s',a')) - Q(s,a)]
        # donde:
        #   - α (alpha) es la tasa de aprendizaje
        #   - γ (gamma) es el factor de descuento futuro
        #   - recompensa es el valor obtenido al realizar la acción
        #   - max(Q(s',a')) es el mejor valor Q en el siguiente estado
        #   - Q(s,a) es el valor Q actual para el estado y acción
        self.Q[pos_actual][mejor_mov] += self.alpha * (reward + self.gamma * q_max_sig - q_actual)

        # Si llege a una meta la marco para no luego no trater de ir hacia ella
        if nueva_posicion in self.laberinto.metas_pos:
            self.metas_visitadas.append(nueva_posicion)

        # Recuerdo las posiciones pasadas con tal de evitar regresar, esto lo penalizaré
        # La idea es que siempre avance, SIEMPRE HACIA LA VICTORIA
        self.posiciones_visitadas.append(nueva_posicion)

        # Decae epsilon cada vez que elige
        self.epsilon = max(self.epsilon * 0.95, 0.01)

        return mejor_mov

    def _calcular_recompensa(self, pos_actual: Coordenada, pos_nueva: Coordenada, casilla):
        """
        Calcula la recompensa obtenida al moverse de una posición a otra en el laberinto.

        Args:
            pos_actual (Coordenada): Posición actual del jugador.
            pos_nueva (Coordenada): Nueva posición tras el movimiento.
            casilla (CasillaLaberinto): Tipo de casilla en la nueva posición.

        Returns:
            float: Recompensa calculada.
        """
        # Distancia Manhattan a la meta más cercana
        metas_no_visitadas = [
            pos for pos in self.laberinto.metas_pos if pos not in self.metas_visitadas
        ]
        if metas_no_visitadas:
            dist_actual = min(pos_actual.distancia_manhatan(meta) for meta in metas_no_visitadas)
            dist_nueva = min(pos_nueva.distancia_manhatan(meta) for meta in metas_no_visitadas)
        else:
            raise MetaNoEncontradaError(
                "Ya no quedan metas, por lo que el programa ya debió de haber finalizado."
            )

        reward = dist_actual - dist_nueva  # positivo si se acercó, negativo si se alejó

        # Recompensas especiales
        if casilla == CasillaLaberinto.META_REAL:
            reward += 50
        elif casilla == CasillaLaberinto.META_FALSA:
            reward -= 50
        # Verificar si una posición ya fue visitada para penalizar los ciclos o regresiones
        elif pos_nueva in self.posiciones_visitadas:
            reward -= 5
        return reward

    def _entrenar(self, n_episodios: int = 10000, max_steps: Optional[int] = None):
        """
        Entrena la política Q-learning mediante simulaciones en laberintos generados.

        Args:
            n_episodios (int): Número de episodios de entrenamiento.
            max_steps (Optional[int]): Máximo de pasos por episodio.
        """
        from laberinto import Laberinto  # Import local para evitar ciclo

        # Cambio self.laberinto para que al ejecutar tick en el laberinto de entrenamiento el jugador use al de entrenamiento
        # Luego hago que use de nuevo el self.laberinto que debe de resolver
        laberinto_original = self.laberinto
        epsilon = self.epsilon

        pasos_maximos = (
            (self.laberinto.filas + self.laberinto.columnas) * 10
            if max_steps is None
            else max_steps
        )

        # Episodios en que se entrena (Se genera la Q-table)
        for ep in range(n_episodios):
            if ep % 10 == 0:
                print(f"Entrenamiento numero {ep + 1}.")

            self.laberinto = Laberinto(
                dimensiones=(self.laberinto.filas, self.laberinto.columnas),
                prob_murallas=self.laberinto.prob_murallas,
                prob_mover_murallas=self.laberinto.prob_mover_murallas,
                n_metas=self.laberinto.n_metas,
                clase_jugador=JugadorQlearningEstrella,
                jugar_instanciado=self,
            )
            self.epsilon = epsilon

            # Se realiza el recorrido del laberinto con un tiempo maximo de entrenamiento (ticks o pasos)
            for _ in range(pasos_maximos):
                self.laberinto.tick()
                if self.laberinto.jugador_gano():
                    break

            self.metas_visitadas = []
            self.posiciones_visitadas.clear()

        # Reinicio las variables a su estado anterior del entrenamiento
        self.laberinto = laberinto_original
        self.epsilon = epsilon

    def mostrar_mapas_calor_Q(self):
        """Muestra un mapa de calor para cada acción en la matriz Q."""
        import matplotlib.pyplot as plt
        import numpy as np

        acciones = list(MovimientosPosibles)
        fig, axs = plt.subplots(1, len(acciones), figsize=(4 * len(acciones), 4))
        for idx, accion in enumerate(acciones):
            matriz_q = np.zeros((self.laberinto.filas, self.laberinto.columnas))
            for i in range(self.laberinto.filas):
                for j in range(self.laberinto.columnas):
                    matriz_q[i, j] = self.Q[Coordenada(i, j)][accion]
            ax = axs[idx] if len(acciones) > 1 else axs
            im = ax.imshow(matriz_q, cmap="hot", interpolation="nearest")
            ax.set_title(f"Acción: {accion.name}")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        plt.suptitle("Mapas de calor Q por acción")
        plt.tight_layout()
        plt.savefig("asd.png")  # Esto porque mi terminal no esta con el modo interactivo activado
