"""Módulo que define la clase Coordenada."""

from dataclasses import dataclass

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

    def desplazar(self, vector) -> "Coordenada":
        """
        Retorna una nueva coordenada desplazada por el vector dado, sin modificar la actual.
        El vector puede ser otra Coordenada, un MovimientosPosibles o un tuple[int, int].
        """
        if isinstance(vector, Coordenada):
            return Coordenada(self.x + vector.x, self.y + vector.y)
        elif isinstance(vector, MovimientosPosibles):
            return Coordenada(self.x + vector.value[0], self.y + vector.value[1])
        elif (
            isinstance(vector, tuple)
            and len(vector) == 2
            and all(isinstance(v, int) for v in vector)
        ):  # Es un tuple[int, int]
            return Coordenada(self.x + vector[0], self.y + vector[1])
        else:
            raise TypeError("El vector debe ser una instancia de Coordenada o MovimientosPosibles")
