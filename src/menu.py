"""
Módulo encargado de mostrar un menú interactivo en la terminal para seleccionar dinámicamente.

Permite elegir un tipo de jugador definido en la carpeta 'jugador'.
"""

import importlib
import os
from typing import Type

import questionary

from jugador import Jugador


def elegir_jugador() -> Type[Jugador]:
    """
    Muestra un menú interactivo en la terminal para seleccionar el tipo de jugador a utilizar.

    El menú se genera dinámicamente buscando todos los módulos Python en la carpeta 'jugador',
    excluyendo archivos especiales y de base. Al seleccionar una opción, se importa el módulo
    correspondiente y se retorna la clase que hereda de Jugador.

    Returns:
        Type[Jugador]: Clase del jugador seleccionado por el usuario.

    Raises:
        SystemExit: Si no hay jugadores disponibles, si la selección es inválida,
        o si no se encuentra una clase válida en el módulo seleccionado.
    """
    jugador_dir = os.path.join(os.path.dirname(__file__), "jugador")
    opciones = []
    nombres_internos = []

    # Buscar dinámicamente todos los jugadores disponibles en la carpeta 'jugador'.
    # Se excluyen archivos especiales y el archivo base 'jugador.py'.
    for filename in os.listdir(jugador_dir):
        if (
            filename.endswith(".py")
            and filename not in ["__init__.py", "jugador.py"]
            and not filename.startswith("_")
        ):
            nombre_interno = filename[:-3]
            nombre_amigable = nombre_interno.replace("_", " ").title()
            opciones.append(nombre_amigable)
            nombres_internos.append(nombre_interno)

    if not opciones:
        print("No hay jugadores disponibles.")
        exit(0)

    # Mostrar el menú interactivo con las opciones de jugadores disponibles usando questionary.
    respuesta = questionary.select("Selecciona el tipo de jugador:", choices=opciones).ask()

    # Obtener el índice de la opción seleccionada
    if respuesta is not None:
        menu_entry_index = opciones.index(respuesta)
    else:
        menu_entry_index = None

    # Importar dinámicamente el módulo correspondiente y buscar la clase de jugador seleccionada.
    if isinstance(menu_entry_index, int):
        jugador_name = nombres_internos[menu_entry_index]

        # Importación dinámica de módulos
        jugador_module = importlib.import_module(f"jugador.{jugador_name}")

        # Buscar la clase que hereda de Jugador en el módulo importado.
        for attr in dir(jugador_module):
            obj = getattr(jugador_module, attr)
            if isinstance(obj, type) and issubclass(obj, Jugador) and obj is not Jugador:
                return obj  # Retorna la clase encontrada

        # Si no se encuentra una clase válida, se informa y termina el programa.
        print(f"No se encontró una clase Jugador en {jugador_name}.")
        exit(1)
    else:
        print("Selección inválida o cancelada.")
        exit(1)
