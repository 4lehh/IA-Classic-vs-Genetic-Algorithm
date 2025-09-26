"""Módulo que define el jugador basado en algoritmo genético para el laberinto."""

from collections import deque
from random import choice, random, uniform
from statistics import stdev
from typing import Optional

from exceptions import MetaNoEncontradaError
from jugador import Jugador
from models import CasillaLaberinto, Coordenada, MovimientosPosibles


class JugadorQlearningAdaptado(Jugador):
    """
    Jugador que combina Q-learning y A* adaptado para aprender a moverse en el laberinto.

    Esta clase fusiona la exploración y aprendizaje de Q-learning con la heurística de búsqueda informada de A*.
    Se creó para que el jugador genético herede de este y no de la clase base Jugador, ya que sus funciones
    son necesarias y está adaptado a las particularidades del algoritmo genético.
    """

    alpha: float  # Tasa de aprendizaje
    gamma: float  # Factor de descuento futuro
    betha: float  # Peso de la Q-table
    omega: float  # Peso de la heurística (distancia a la meta)
    epsilon: float  # Nivel de exploración
    posicion_inicial: Optional[Coordenada] = None
    Q: dict[
        Coordenada, dict[MovimientosPosibles, float]
    ]  # Tabla que representa, por cada posicion, que acciones podemos tomar, y por cada una de estas, cual es el valor que nos aporta tomar dicha accion
    metas_visitadas: list[Coordenada]
    posiciones_visitadas: deque[Coordenada]

    def __init__(
        self,
        laberinto,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        betha: float = 0.5,
        omega: float = 0.5,
    ):
        """
        Inicializa una instancia de JugadorQlearningAdaptado.

        Args:
            laberinto: Instancia del laberinto sobre el que se juega.
            alpha: Tasa de aprendizaje.
            gamma: Factor de descuento futuro.
            epsilon: Nivel de exploración.
            betha: Peso de la Q-table.
            omega: Peso de la heurística (distancia a la meta).
        """
        super().__init__(laberinto)
        self.alpha = alpha
        self.gamma = gamma
        self.betha = betha
        self.omega = omega
        self.epsilon = epsilon
        self.Q = {}
        self.metas_visitadas = []
        self.posiciones_visitadas = deque(maxlen=10)

        self._inicializar_Q_table()
        self._entrenar(100)
        # self.mostrar_mapas_calor_Q()

    def _seleccionar_meta(self) -> Coordenada:
        """
        Selecciona la meta no visitada más cercana al jugador (según distancia Manhattan).

        Si hay varias metas a la misma distancia mínima, selecciona una al azar entre ellas.

        Returns:
            Coordenada: Posición de la meta seleccionada.
        Raises:
            MetaNoEncontradaError: Si no hay metas disponibles para dirigirse.
        """
        metas_mas_cercanas = self.laberinto.metas_mas_cercanas_a_posicion(
            self.laberinto.jugador_pos, self.metas_visitadas
        )

        if not metas_mas_cercanas:
            raise MetaNoEncontradaError("No hay metas a las cuales dirigirse.")

        return choice(metas_mas_cercanas)

    def _eleccion_moverse(
        self, movimientos_validos: list[MovimientosPosibles]
    ) -> MovimientosPosibles:
        """
        Elige el movimiento óptimo combinando la política Q-learning y la heurística A*.

        Si el agente decide explorar (según epsilon), elige un movimiento aleatorio.
        Si explota, pondera el valor Q de cada acción y la distancia a la meta más cercana,
        buscando maximizar la recompensa esperada y minimizar la distancia heurística.

        Args:
            movimientos_validos: Movimientos posibles para el jugador.

        Returns:
            Movimiento seleccionado por la combinación de Q-learning y A*.
        """
        if self.posicion_inicial is None:
            self.posicion_inicial = self.laberinto.jugador_pos

        pos_actual = self.laberinto.jugador_pos
        mejor_mov = None
        mejor_balance = float("-inf")

        # Decisión: explorar o explotar
        if random() < self.epsilon:
            mejor_mov = choice(movimientos_validos)
        else:
            q_vals = {mov: self.Q[pos_actual][mov] for mov in movimientos_validos}
            meta_objetivo = self._seleccionar_meta()
            for mov, valor_q in q_vals.items():
                balance = self.betha * valor_q - self.omega * meta_objetivo.distancia_euclidiana(
                    pos_actual + mov
                )
                if balance > mejor_balance or mejor_mov is None:
                    mejor_balance = balance
                    mejor_mov = mov

            if mejor_mov is None:
                return MovimientosPosibles.NO_MOVERSE

        nueva_posicion = pos_actual + mejor_mov

        if not self.laberinto.coordenada_en_laberinto(nueva_posicion):
            return MovimientosPosibles.NO_MOVERSE

        reward = self._calcular_recompensa(
            pos_actual, nueva_posicion, self.laberinto.get_casilla(nueva_posicion)
        )

        # Actualizar Q-table usando la ecuacion de Q-learning
        q_actual = self.Q[pos_actual][mejor_mov]
        q_max_sig = max(self.Q[nueva_posicion].values())
        self.Q[pos_actual][mejor_mov] += self.alpha * (reward + self.gamma * q_max_sig - q_actual)

        if nueva_posicion in self.laberinto.metas_pos:
            self.metas_visitadas.append(nueva_posicion)

        self.posiciones_visitadas.append(nueva_posicion)
        self.epsilon = max(self.epsilon * 0.95, 0.01)
        return mejor_mov

    def _calcular_recompensa(
        self, pos_actual: Coordenada, pos_nueva: Coordenada, casilla: CasillaLaberinto
    ) -> float:
        """
        Calcula la recompensa obtenida al moverse de una posición a otra en el laberinto.

        Args:
            pos_actual: Posición actual del jugador.
            pos_nueva: Nueva posición tras el movimiento.
            casilla: Tipo de casilla en la nueva posición.

        Returns:
            Recompensa calculada.
        """
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
            reward -= 10
        if len(self.posiciones_visitadas) >= 2 and pos_nueva == self.posiciones_visitadas[-2]:
            reward -= 20  # penaliza retroceder al estado anterior inmediato
        return reward

    def _entrenar(self, n_episodios: int = 10000, max_steps: Optional[int] = None):
        """
        Entrena la política Q-learning mediante simulaciones en laberintos generados.

        Args:
            n_episodios: Número de episodios de entrenamiento.
            max_steps: Máximo de pasos por episodio.
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
            self.laberinto = Laberinto(
                dimensiones=(self.laberinto.filas, self.laberinto.columnas),
                prob_murallas=self.laberinto.prob_murallas,
                prob_mover_murallas=self.laberinto.prob_mover_murallas,
                n_metas=self.laberinto.n_metas,
                clase_jugador=JugadorQlearningAdaptado,
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
        """
        Muestra un mapa de calor para cada acción en la matriz Q.

        Guarda la imagen como 'asd.png'.
        """
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

    def desempeno(self) -> float:
        """
        Calcula el desempeño del jugador: combina cercanía a la meta y eficiencia (menos ticks).

        Returns:
            Desempeño como valor float.
        """
        distancia = self.laberinto.jugador_pos.distancia_euclidiana(self.laberinto.meta_real_pos)

        # Normalizamos eficiencia (menos ticks => valor más alto)
        eficiencia = 1 / (1 + self.cantidad_tick)

        if distancia == 0:
            # Llegó a la meta: bonificación clara + eficiencia
            bonus = 2.0  # <-- aquí ajustas el "premio por ganar"
            return bonus + eficiencia

        # Normalizamos cercanía (más cerca => valor más alto)
        cercania = 1 / (1 + distancia)

        # Combinar con pesos ajustables
        w_cercania = 0.8
        w_eficiencia = 0.2
        return w_cercania * cercania + w_eficiencia * eficiencia

    def _inicializar_Q_table(self):
        """Inicializa la Q-table para todas las posiciones posibles del laberinto."""
        for i in range(self.laberinto.filas):
            for j in range(self.laberinto.columnas):
                self.Q[Coordenada(i, j)] = {mov: 0.0 for mov in MovimientosPosibles}

    def __lt__(self, other: "JugadorQlearningAdaptado") -> bool:
        """Permite comparar dos jugadores por desempeño."""
        return self.desempeno() < other.desempeno()


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

        print(
            f"Parámetros óptimos encontrados: {self.alpha=}, {self.gamma=}, {self.betha=}, {self.omega=}"
        )

        self.Q = {}
        self.metas_visitadas = []
        self.posiciones_visitadas = deque(maxlen=10)

        self._inicializar_Q_table()
        self._entrenar()
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
                print("Población inicial creada.")
            else:
                self.lista_generaciones = sorted(self.lista_generaciones, reverse=True)
                mejor_jugador = self.lista_generaciones[0]
                segundo_mejor_jugador = self.lista_generaciones[1]
                self._crossover_and_mutation(mejor_jugador, segundo_mejor_jugador)

            print(f"Generación número {gen_num + 1}.")
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
