from cuadrilla import Cuadrilla
import os

def main() -> None:
    cuadrilla = Cuadrilla(dimensiones=10, dificultad=2)

    # Probar iteraciones
    for _ in range(10):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola
        print(cuadrilla)
        cuadrilla.cambiar_muros()
        input("Presiona Enter para continuar...")  # Pausa hasta que el usuario presione Enter

if __name__ == "__main__":
    main()
