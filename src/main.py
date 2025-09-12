import os

from laberinto import Laberinto


def simular_laberinto(laberinto: Laberinto):
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
            laberinto.imprimir()
            opcion = (
                input("Presiona Enter para continuar, 'q' o 'exit' para salir:\n> ").strip().lower()
            )
            if opcion in ["q", "exit"]:
                print("Saliendo...")
                break

            laberinto.tick()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")


def main() -> None:
    laberinto = Laberinto(
        dimenciones=(20, 20), prob_murallas=0.3, prob_mover_murallas=0.01, n_metas=3
    )
    simular_laberinto(laberinto)


if __name__ == "__main__":
    main()
