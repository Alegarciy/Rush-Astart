from dataclasses import dataclass
from typing import Tuple
from Tablero.cosntantes import EJE_X, EJE_Y
from Tablero.movimiento import Movimiento


@dataclass(frozen=True)
class Vehiculo:
    id: int
    # La lista de casillas se visualiza [ [y,x] , [y,x] , [y,x] ]
    casillas: Tuple[Tuple[int, int]]
    orientacionHorizontal: bool

    # La funcion retorna un nuevo vehiculo, no actualiza el mismo
    def mover(self, movimiento: Movimiento) -> "Vehiculo":
        casillasActualizadas = []

        # Genera un neuvo posicionamiento de cada casilla
        for casilla in self.casillas:
            casillasActualizadas.append(
                self.actualizarCasillaConMovimiento(casilla, movimiento))
        return Vehiculo(id=self.id, casillas=casillasActualizadas, orientacionHorizontal=self.orientacionHorizontal)

    # Funcion que actualiza el estado del vehiculo basado en el desplazamiento del movimiento
    def actualizarCasillaConMovimiento(self, casilla, movimiento: Movimiento):
        posicionActualX = casilla[EJE_X]
        posicionActualY = casilla[EJE_Y]

        # Retorna nueva posicion
        if(self.orientacionHorizontal):
            return [posicionActualY, posicionActualX + movimiento.desplazamiento]
        return [posicionActualY + movimiento.desplazamiento, posicionActualX]
