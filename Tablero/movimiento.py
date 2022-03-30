from dataclasses import dataclass

# la clase movimiento, es la encargada de la transicion de estado,
# pues indica el movimiento para el nuevo estado del tablero


@dataclass(frozen=True)
class Movimiento:
    idVehiculo: int = -1
    inidiceVehiculo: int = -1
    desplazamiento: int = 0
