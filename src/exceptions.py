"""Modulo que define las distintas excepciones custom del proyecto."""


class JugadorError(Exception):
    """Excepción base para errores del jugador."""


class MovimientoInvalidoError(Exception):
    """Se lanza cuando el movimiento es inválido."""


class MetaNoEncontradaError(Exception):
    """Se lanza cuando no se encuentra una meta en el laberinto."""


class CreacionLaberintoError(Exception):
    """Se lanza cuando falla la creacion del Laberinto."""


class NotImplementedError(Exception):
    """Lo que lanza este error aun no se a terminado de implementar."""
