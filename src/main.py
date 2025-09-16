"""Módulo principal para la simulación y manejo del laberinto."""

from jugador import JugadorAEstrella, JugadorGreedy, JugadorQlearning, JugadorRandom
from laberinto import Laberinto
from simulacion import simular_laberinto


def main():
    """Función principal que ejecuta la simulación del laberinto."""
    laberinto = Laberinto(
        dimensiones=(20, 20),
        prob_murallas=0.2,
        prob_mover_murallas=0.01,
        n_metas=3,
        clase_jugador=JugadorGreedy,
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
