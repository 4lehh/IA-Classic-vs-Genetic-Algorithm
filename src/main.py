"""Módulo principal para la simulación y manejo del laberinto."""

import os

from laberinto import Laberinto

SALIR = True
CONTINUAR = False


def manejar_opcion_salida_espera() -> bool:
    """Maneja la opción de salida o espera del usuario en el menú principal."""
    opcion = input("Presiona Enter para continuar, 'q' o 'exit' para salir:\n> ").strip().lower()
    if opcion in ["q", "exit"]:
        print("Saliendo...")
        return SALIR
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
    try:
        while True:
            mover_murallas_imprimir_laberinto(laberinto=laberinto)
            if manejar_opcion_salida_espera() == SALIR:
                break

            mover_jugador_imprimir_laberinto(laberinto=laberinto)

            if laberinto.jugador_gano():
                print("LLEGO A LA META!!!")
                print(f"Se demoro {laberinto.ticks_transcurridos} ticks.")
                exit(0)

            if manejar_opcion_salida_espera() == SALIR:
                break

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        exit(0)


def main():
    """Función principal que ejecuta la simulación del laberinto."""
    laberinto = Laberinto(
        dimenciones=(20, 20), prob_murallas=0.3, prob_mover_murallas=0.01, n_metas=3
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
