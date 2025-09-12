import os

from laberinto import Laberinto

SALIR = True
CONTINUAR = False


def manejar_opcion_salida_espera() -> bool:
    opcion = input("Presiona Enter para continuar, 'q' o 'exit' para salir:\n> ").strip().lower()
    if opcion in ["q", "exit"]:
        print("Saliendo...")
        return SALIR
    return CONTINUAR


def mover_murallas_imprimir_laberinto(laberinto: Laberinto):
    laberinto.mover_murallas()

    os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
    laberinto.imprimir()


def mover_jugador_imprimir_laberinto(laberinto: Laberinto):
    laberinto.mover_jugador()

    os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
    laberinto.imprimir()


def simular_laberinto(laberinto: Laberinto):
    try:
        while True:
            mover_murallas_imprimir_laberinto(laberinto=laberinto)
            if manejar_opcion_salida_espera() == SALIR:
                break

            mover_jugador_imprimir_laberinto(laberinto=laberinto)
            if manejar_opcion_salida_espera() == SALIR:
                break

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        exit(0)


def main():
    laberinto = Laberinto(
        dimenciones=(20, 20), prob_murallas=0.3, prob_mover_murallas=0.01, n_metas=3
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
