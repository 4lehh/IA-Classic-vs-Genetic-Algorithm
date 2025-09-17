"""Módulo principal para la simulación y manejo del laberinto."""

from laberinto import Laberinto
from menu import elegir_jugador
from simulacion import simular_laberinto


def main():
    """Función principal que ejecuta la simulación del laberinto."""
    tipo_jugador = elegir_jugador()

    laberinto = Laberinto(
        dimensiones=(20, 20),
        prob_murallas=0.2,
        prob_mover_murallas=0.01,
        n_metas=3,
        clase_jugador=tipo_jugador,
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
