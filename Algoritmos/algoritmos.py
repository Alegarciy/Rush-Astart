import collections
import heapq
from dataclasses import dataclass
from lib2to3.pytree import Node
from typing import List, Set

from Tablero.tablero import Tablero
from Tablero.nodo import Nodo, NodoHijo


class NoSolutionFoundException(Exception):
    pass


@dataclass(frozen=True)
class Resultado:
    nodoFinal: Nodo
    numeroDeEstadosVisitados: int


def aEstrella(tablero: Tablero, profundidadMaxima: int = 100) -> Resultado:
    profundidad = 0
    # lista de estados cerrados
    nodosVisitados: Set[Tablero] = set()
    listaOrdenada: List[Nodo] = list()
    raiz = Nodo(tablero, profundidad)
    heapq.heappush(listaOrdenada, raiz)

    if raiz.tablero.esConfiguracionFinal():
        return Resultado(raiz, len(nodosVisitados))

    while len(listaOrdenada) & profundidad < profundidadMaxima:
        nodoActual = heapq.heappop(listaOrdenada)
        profundidad = nodoActual.profundidad
        for movimientoPosible in nodoActual.tablero.getMovimientos():
            tableroHijo = nodoActual.tablero.moverVehiculo(
                movimiento=movimientoPosible)

            # Todo: do it manually
            if tableroHijo not in nodosVisitados:
                nodosVisitados.add(tableroHijo)
                nodo = NodoHijo(
                    tablero=tableroHijo,
                    padre=nodoActual,
                    profundidad=profundidad + 1,
                    valor=tableroHijo.getCostoMinimo() + profundidad
                )
                heapq.heappush(listaOrdenada, nodo)

                if tableroHijo.esConfiguracionFinal():
                    return Resultado(nodo, len(nodosVisitados))

    raise NoSolutionFoundException
