import argparse
from typing import Type

from jugador import (
    Jugador,
    JugadorAEstrella,
    JugadorGenetico,
    JugadorGreedy,
    JugadorQlearning,
    JugadorQlearningEstrella,
    JugadorRandom,
)
from laberinto import Laberinto
from menu import elegir_jugador
from simulacion import simular_experimento, simular_laberinto


def main():
    # Diccionario: nombre en minúsculas -> clase
    clases: dict[str, Type[Jugador]] = {
        cls.__name__: cls
        for cls in [
            JugadorAEstrella,
            JugadorGenetico,
            JugadorGreedy,
            JugadorQlearning,
            JugadorQlearningEstrella,
            JugadorRandom,
        ]
    }
    parser = argparse.ArgumentParser(description="Selecciona el algoritmo a ejecutar.")
    parser.add_argument(
        "-a",
        "--algoritmo",
        choices=list(clases.keys()),
        required=False,
        help="Algoritmo a ejecutar",
    )
    parser.add_argument("-i", "--interactivo", action="store_true", help="Modo interactivo")
    parser.add_argument(
        "-d",
        "--dimensiones",
        type=int,
        nargs=2,
        metavar=("FILAS", "COLUMNAS"),
        default=(20, 20),
        help="Dimensiones del laberinto (filas columnas), por defecto 20 20",
    )
    parser.add_argument(
        "-pg",
        "--prob-gen-murallas",
        type=float,
        default=0.2,
        help="Probabilidad de generar murallas (default: 0.2)",
    )
    parser.add_argument(
        "-pm",
        "--prob-mover-murallas",
        type=float,
        default=0.01,
        help="Probabilidad de mover murallas (default: 0.01)",
    )
    parser.add_argument("-e", "--experiments", action="store_true", help="Modo experimentación")
    parser.add_argument("--n-metas", type=int, default=3, help="Cantidad de metas (default: 3)")
    args = parser.parse_args()

    if not args.interactivo and not args.algoritmo:
        parser.error(
            "El argumento -a/--algoritmo es obligatorio si no se usa el modo interactivo (-i/--interactivo)."
        )

    # Selección de clase de jugador
    tipo_jugador = None
    if args.algoritmo:
        tipo_jugador = clases[args.algoritmo]
    elif args.interactivo and not args.algoritmo:
        tipo_jugador = elegir_jugador()

    if tipo_jugador is None:
        parser.error("No se seleccionó un tipo de jugador válido.")

    laberinto = Laberinto(
        dimensiones=tuple(args.dimensiones),
        prob_murallas=args.prob_gen_murallas,
        prob_mover_murallas=args.prob_mover_murallas,
        n_metas=args.n_metas,
        clase_jugador=tipo_jugador,
    )

    if args.experiments:
        simular_experimento(laberinto)
    else:
        simular_laberinto(laberinto, modo_interactivo=args.interactivo)


if __name__ == "__main__":
    main()
