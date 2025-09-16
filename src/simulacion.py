import os
from enum import Enum, auto

from exceptions import (
    CreacionLaberintoError,
    MetaNoEncontradaError,
    MovimientoInvalidoError,
    NotImplementedError,
)
from laberinto import Laberinto

LIMITE_DE_TICKS_DE_SIMULACION = 10000


class EstadoSimulacion(Enum):
    SALIR = auto()
    CONTINUAR = auto()
    AUTO = auto()


def manejar_opcion_salida_espera() -> EstadoSimulacion:
    """Maneja las opciones del usuario en el menú principal."""
    opcion = (
        input(
            "Presiona Enter para continuar\n'a' o 'auto' para que avance automáticamente el juego\n'q' o 'exit' para salir:\n> "
        )
        .strip()
        .lower()
    )
    if opcion in ["q", "exit"]:
        print("Saliendo...")
        return EstadoSimulacion.SALIR
    if opcion in ["auto", "a"]:
        return EstadoSimulacion.AUTO
    return EstadoSimulacion.CONTINUAR


def controlar_flujo(preguntar: bool) -> tuple[bool, bool]:
    """
    Controla el flujo de la simulación según la interacción del usuario.

    Dependiendo del valor de 'preguntar', decide si se debe mostrar el menú de opciones al usuario
    para continuar, autoavanzar o salir de la simulación.

    Args:
        preguntar (bool): Si True, se pregunta al usuario por la siguiente acción.

    Returns:
        tuple[bool, bool]:
            - El primer valor indica si se debe seguir preguntando al usuario (modo manual).
            - El segundo valor indica si se debe salir de la simulación.

    Ejemplo de uso:
        preguntar, salir = controlar_flujo(preguntar)
        if salir:
            break
    """
    if preguntar:
        opcion = manejar_opcion_salida_espera()
        if opcion == EstadoSimulacion.SALIR:
            return preguntar, True
        if opcion == EstadoSimulacion.AUTO:
            return False, False
    return preguntar, False


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


def simular_laberinto(laberinto):
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
                print("Se superó el límite de tiempo de simulación.")
                break

            mover_murallas_imprimir_laberinto(laberinto=laberinto)
            preguntar, salir = controlar_flujo(preguntar)
            if salir:
                break

            mover_jugador_imprimir_laberinto(laberinto=laberinto)
            if laberinto.jugador_gano():
                print("¡LLEGÓ A LA META!")
                print(f"Se demoró {laberinto.ticks_transcurridos} ticks.")
                exit(0)

            preguntar, salir = controlar_flujo(preguntar)
            if salir:
                break
            contador += 1

    except CreacionLaberintoError as e:
        print(f"Error al crear el laberinto: {e}")
    except MovimientoInvalidoError as e:
        print(f"Error de movimiento: {e}")
    except MetaNoEncontradaError as e:
        print(f"Error de meta: {e}")
    except NotImplementedError as e:
        print(f"No implementado: {e}")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        exit(0)
