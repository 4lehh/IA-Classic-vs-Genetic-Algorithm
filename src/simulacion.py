"""Módulo que contiene la lógica de simulación del laberinto y control de flujo de usuario."""

import os
from enum import Enum, auto

from exceptions import (
    CreacionLaberintoError,
    MetaNoEncontradaError,
    MovimientoInvalidoError,
)
from laberinto import Laberinto


class EstadoSimulacion(Enum):
    """
    Enum que representa los posibles estados de la simulación del laberinto.

    SALIR: Terminar la simulación.
    CONTINUAR: Continuar paso a paso (modo manual).
    AUTO: Ejecutar automáticamente sin intervención del usuario.
    """

    SALIR = auto()
    CONTINUAR = auto()
    AUTO = auto()


def manejar_opcion_salida_espera() -> EstadoSimulacion:
    """
    Solicita al usuario una opción para controlar la simulación.

    Returns:
        EstadoSimulacion: Estado elegido por el usuario (SALIR, CONTINUAR, AUTO).
    """
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

    Si 'preguntar' es True, solicita al usuario la siguiente acción (continuar, auto, salir).
    Si es False, continúa automáticamente.

    Args:
        preguntar (bool): Si True, se pregunta al usuario por la siguiente acción.

    Returns:
        tuple[bool, bool]:
            - El primer valor indica si se debe seguir preguntando al usuario (modo manual).
            - El segundo valor indica si se debe salir de la simulación.
    """
    if preguntar:
        opcion = manejar_opcion_salida_espera()
        if opcion == EstadoSimulacion.SALIR:
            return preguntar, True
        if opcion == EstadoSimulacion.AUTO:
            return False, False
    return preguntar, False


def limpiar_e_imprimir_laberinto(laberinto: Laberinto):
    """
    Limpia la consola y muestra el estado actual del laberinto.

    Args:
        laberinto (Laberinto): Instancia del laberinto a imprimir.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Limpia la consola
    laberinto.imprimir()


def simular_laberinto(
    laberinto: Laberinto, limite_de_ticks: int = 10000, modo_interactivo: bool = False
):
    """
    Ejecuta la simulación del laberinto, moviendo murallas y jugador en cada tick.

    Args:
        laberinto (Laberinto): Instancia del laberinto a simular.
        limite_de_ticks (int, opcional): Máximo de ciclos de simulación. Por defecto 10000.
        modo_interactivo (bool, opcional): Si True, permite interacción paso a paso con el usuario.

    El modo interactivo permite continuar, autoavanzar la simulación o salir según la entrada del usuario.
    Si el jugador llega a la meta, muestra un mensaje y termina la simulación.
    Maneja errores comunes y permite interrupción con Ctrl+C.
    """
    preguntar = True
    contador = 0
    try:
        while contador < limite_de_ticks:
            laberinto.mover_murallas()
            laberinto.mover_jugador()

            if modo_interactivo:
                limpiar_e_imprimir_laberinto(laberinto)

            if laberinto.jugador_gano():
                if modo_interactivo:
                    print("¡LLEGÓ A LA META!")
                    print(f"Se demoró {laberinto.ticks_transcurridos} ticks.")
                else:
                    print(f"{laberinto.ticks_transcurridos=}")
                exit(0)

            if modo_interactivo:
                preguntar, salir = controlar_flujo(preguntar)
                if salir:
                    break

            contador += 1

        else:
            if modo_interactivo:
                print("Se superó el límite de tiempo de simulación.")

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
