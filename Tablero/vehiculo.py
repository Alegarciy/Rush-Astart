from dataclasses import dataclass
from typing import Tuple
from Tablero.cosntantes import EJE_X, EJE_Y
from Tablero.movimiento import Movimiento


@dataclass(frozen=True)
class Vehiculo:
    id: int
    casillas: Tuple[Tuple[int, int]]
    orientacionHorizontal: bool

    # La funcion retorna un nuevo vehiculo, no actualiza el mismo
    def mover(self, movimiento: Movimiento) -> "Vehiculo":
        casillasActualizadas = tuple(
            map(
                lambda x: (x[0], x[1] + movimiento.desplazamiento)
                if self.orientacionHorizontal
                else (x[0] + movimiento.desplazamiento, x[1]),
                self.casillas,
            )
        )
        return Vehiculo(id=self.id, casillas=casillasActualizadas, orientacionHorizontal=self.orientacionHorizontal)
