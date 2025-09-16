"""Módulo principal para la simulación y manejo del laberinto."""

import os

from jugador import JugadorAEstrella, JugadorQlearning, JugadorRandom
from laberinto import Laberinto

SALIR = 1
CONTINUAR = 0
AUTO = 2

LIMITE_DE_TICKS_DE_SIMULACION = 10000


def manejar_opcion_salida_espera() -> int:
    """Maneja la opción de salida o espera del usuario en el menú principal."""
    opcion = (
        input(
            "Presiona Enter para continuar\n'a' o 'auto' para que avanze automaticmente el juego\n'q' o 'exit' para salir:\n> "
        )
        .strip()
        .lower()
    )
    if opcion in ["q", "exit"]:
        print("Saliendo...")
        return SALIR
    if opcion in ["auto", "a"]:
        return AUTO
    return CONTINUAR


def mover_murallas_imprimir_laberinto(laberinto: Laberinto):
    """
    Mueve las murallas y muestra el laberinto actualizado.

    Args:
        laberinto: Instancia del laberinto a modificar.
    """
    laberinto.mover_murallas()

    os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
    laberinto.imprimir()


def mover_jugador_imprimir_laberinto(laberinto: Laberinto):
    """
    Mueve el jugador y muestra el laberinto actualizado.

    Args:
        laberinto: Instancia del laberinto a modificar.
    """
    laberinto.mover_jugador()

    os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
    laberinto.imprimir()


def simular_laberinto(laberinto: Laberinto):
    """
    Simula el avance del jugador y murallas en el laberinto.

    Args:
        laberinto: Instancia del laberinto a simular.
    """

    preguntar = True
    contador = 0
    try:
        while True:
            if contador >= LIMITE_DE_TICKS_DE_SIMULACION:
                print("Se supero el limite de tiempo de simulacion.")
                break

            mover_murallas_imprimir_laberinto(laberinto=laberinto)
            if preguntar:
                opcion = manejar_opcion_salida_espera()
                if opcion == SALIR:
                    break
                if opcion == AUTO:
                    preguntar = False

            mover_jugador_imprimir_laberinto(laberinto=laberinto)

            if laberinto.jugador_gano():
                print("LLEGO A LA META!!!")
                print(f"Se demoro {laberinto.ticks_transcurridos} ticks.")
                exit(0)

            if preguntar:
                opcion = manejar_opcion_salida_espera()
                if opcion == SALIR:
                    break
                if opcion == AUTO:
                    preguntar = False

            contador += 1

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        exit(0)


def main():
    """Función principal que ejecuta la simulación del laberinto."""
    laberinto = Laberinto(
        dimenciones=(20, 20),
        prob_murallas=0.2,
        prob_mover_murallas=0.01,
        n_metas=3,
        clase_jugador=JugadorAEstrella,
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
