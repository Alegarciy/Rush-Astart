from dataclasses import dataclass

from Tablero.tablero import Tablero

@dataclass(frozen=True)
class Nodo:
  tablero: Tablero= Tablero(ancho=0, vehiculos=tuple())
  profundidad: int= 0
  valor: int= 0

  def __lt__(self, otroNodo):
    return self.valor < otroNodo.valor

@dataclass(frozen=True)
class NodoHijo(Nodo):
  padre: Nodo = Nodo()
