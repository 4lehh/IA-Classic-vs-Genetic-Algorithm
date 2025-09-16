"""Módulo que define la clase Coordenada."""

from dataclasses import dataclass
from typing import Union

from movimientos import MovimientosPosibles


@dataclass(frozen=True)
class Coordenada:
    """
    Clase que representa una coordenada en un espacio 2D.

    Se utiliza @dataclass(frozen=True) para hacer la clase inmutable y hashable.
    Esto permite usar instancias de Coordenada como claves en diccionarios y elementos en conjuntos (set).
    """

    x: int
    y: int

    def __iter__(self):
        """
        Permite iterar sobre la instancia para obtener sus componentes (x, y).
        Esto habilita la descompresión: x, y = coordenada
        """
        yield self.x
        yield self.y

    def __add__(self, other: "Union[Coordenada, MovimientosPosibles, tuple[int, int]]"):
        """
        Suma la coordenada actual con otra Coordenada, MovimientosPosibles o una tupla de dos enteros.
        """
        if isinstance(other, Coordenada):
            return Coordenada(self.x + other.x, self.y + other.y)
        elif isinstance(other, MovimientosPosibles):
            return Coordenada(self.x + other.value[0], self.y + other.value[1])
        elif (
            isinstance(other, tuple) and len(other) == 2 and all(isinstance(v, int) for v in other)
        ):  # Es un tuple[int, int]
            return Coordenada(self.x + other[0], self.y + other[1])
        else:
            raise TypeError(
                "Una coordenada solo se puede sumar con una instancia de Coordenada, MovimientosPosibles o tuple[int, int]"
            )

    def __sub__(self, other: "Union[Coordenada, MovimientosPosibles, tuple[int, int]]"):
        """
        Resta la coordenada actual con otra Coordenada, MovimientosPosibles o una tupla de dos enteros.
        """
        if isinstance(other, Coordenada):
            return Coordenada(self.x - other.x, self.y - other.y)
        elif isinstance(other, MovimientosPosibles):
            return Coordenada(self.x - other.value[0], self.y - other.value[1])
        elif (
            isinstance(other, tuple) and len(other) == 2 and all(isinstance(v, int) for v in other)
        ):  # Es un tuple[int, int]
            return Coordenada(self.x - other[0], self.y - other[1])
        else:
            raise TypeError(
                "Una coordenada solo se puede restar con una instancia de Coordenada, MovimientosPosibles o tuple[int, int]"
            )

    def distancia_euclidiana(self, otra: "Coordenada") -> float:
        """
        Calcula la distancia euclidiana entre esta coordenada y otra.
        """
        return ((self.x - otra.x) ** 2 + (self.y - otra.y) ** 2) ** 0.5

    def distancia_manhatan(self, otra: "Coordenada") -> int:
        """
        Calcula la distancia de Manhattan entre esta coordenada y otra.
        """
        return abs(self.x - otra.x) + abs(self.y - otra.y)
