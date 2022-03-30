from csv import reader
from dataclasses import dataclass, replace
from typing import Iterator, List, Tuple

from Tablero.cosntantes import EJE_X, EJE_Y, VEHICULO_FRENTE, VEHICULO_ATRAS, VEHICULO_ROJO
from Tablero.movimiento import Movimiento
from Tablero.vehiculo import Vehiculo

# Cada tablero va a ser un estado nuevo del nodo,
# entonces no lo acutalizamos, generamos uno nuevo


@dataclass(frozen=True)
class Tablero:
    ancho: int  # dimensiones del tablero anchoXancho
    vehiculos: Tuple[Vehiculo]

    # Genera nuevo tablero con el posicionamiento de los vehiculos actualizadoss
    def moverVehiculo(self, movimiento: Movimiento) -> "Tablero":
        indiceVehiculoSeleccionado = movimiento.inidiceVehiculo
        vehiculoActualizado = self.vehiculos[indiceVehiculoSeleccionado].mover(
            movimiento)

        # Generar nuevo posicionamiento de vehiculos
        vehiculosActualizados = (
            self.vehiculos[0: indiceVehiculoSeleccionado]
            + [vehiculoActualizado]
            + self.vehiculos[indiceVehiculoSeleccionado + 1:]
        )
        return replace(self, vehiculos=vehiculosActualizados)

    # genera mapa de vehiculos indexados [llave: id_vehiculo, contenido: vehiculo: Vehiculo]
    @staticmethod
    def generarMapaDeVehiculos(matriz: List[List[int]]):
        vehiculosGuardados = dict()
        for indiceFila, fila in enumerate(matriz):
            # contiene los numeros de vehiculo
            for indiceColumna, columna in enumerate(fila):
                if columna not in vehiculosGuardados:
                    vehiculosGuardados[columna] = [
                        (indiceFila, indiceColumna)]
                else:
                    vehiculosGuardados[columna].append(
                        (indiceFila, indiceColumna))

        return vehiculosGuardados

    # Metodo que recibe una matriz y retorna un tablero => necesario para generar un tablero
    @staticmethod
    def generarTableroDeMatriz(matriz: List[List[int]]) -> "Tablero":

        # validacion de si la matriz es correcta
        if(len(matriz) != 6 or len(matriz) != len(matriz[0])):
            raise Exception(
                "Error: la matriz del archivo no es una matriz de dimensiones 6x6"
            )
        else:
            vehiculosGuardados = Tablero.generarMapaDeVehiculos(matriz)
            vehiculosDeNuevoTablero = tuple()

            for idVehiculo, casillas in sorted(vehiculosGuardados.items()):
                if(idVehiculo >= 0):
                    esHorizontal = casillas[VEHICULO_ATRAS][0] == casillas[VEHICULO_FRENTE][0]
                    vehiculoGenerado = Vehiculo(
                        id=idVehiculo,
                        casillas=casillas,
                        orientacionHorizontal=esHorizontal
                    )
                    vehiculosDeNuevoTablero = vehiculosDeNuevoTablero + \
                        (vehiculoGenerado, )

            return Tablero(len(matriz), vehiculos=vehiculosDeNuevoTablero)

    def esConfiguracionFinalFinal(self) -> bool:
        return self.vehiculos[VEHICULO_ROJO].casillas[VEHICULO_FRENTE][EJE_X] == self.ancho - 1

    # Minimo para despejar ruta del carro Rojo
    def MinimoDePasosParaDespejarPaso(self) -> int:
        casillasPorCubrir = self.getCasillasPorCubrir()
        minimoDePasos = 0

        for vehiculoObstruyendo in self.getVehiculosObstruyendoPaso():
            if len(vehiculoObstruyendo.casillas) < 2:
                minimoDePasos += 1
            else:
                for casilla in casillasPorCubrir:
                    try:
                        indiceDeCasilla = vehiculoObstruyendo.casillas.index(
                            casilla)
                        minimoDePasos += min(
                            indiceDeCasilla + 1,  # movimiento para arriba de un carro de dos casillas
                            len(vehiculoObstruyendo.casillas) - indiceDeCasilla
                        )
                    except ValueError:
                        continue
        return minimoDePasos

    def getVehiculosObstruyendoPaso(self) -> Iterator[Vehiculo]:
        casillasPorCubrir = self.getCasillasPorCubrir()
        for vehiculo in self.vehiculos:
            if any(casillaPorCubrir for casillaPorCubrir in casillasPorCubrir if casillaPorCubrir in vehiculo.casillas):
                yield vehiculo

    # Reperesenta las casillas por cubrir del carro rojo
    def getCasillasPorCubrir(self):
        return [
            (self.vehiculos[VEHICULO_ROJO].casillas[VEHICULO_FRENTE][EJE_Y], pos)
            for pos in range(self.vehiculos[VEHICULO_ROJO].casillas[VEHICULO_FRENTE][EJE_X] + 1, self.ancho)
        ]

    # Calcula los movimientos posibles de los vehiculo para generar los nuevos estados
    # en este momento todos los movimentos tienen el mismo peso
    # Todo: ajustar el peso de los movimentos para una regla nueva
    def getMovimientos(self) -> Iterator[Movimiento]:
        # recorremos cada vehiculo del tablero
        for indice, vehiculo in enumerate(self.vehiculos):
            casillaTrasera = None
            casillaDelantera = None
            desplazamientoHortizontal = 1 if vehiculo.orientacionHorizontal else 0
            desplazamientoVertical = abs(desplazamientoHortizontal - 1)

            if vehiculo.casillas[VEHICULO_ATRAS][desplazamientoHortizontal] > 0:
                casillaTrasera = (
                    vehiculo.casillas[VEHICULO_ATRAS][EJE_Y] -
                    desplazamientoVertical,
                    vehiculo.casillas[VEHICULO_ATRAS][EJE_X] -
                    desplazamientoHortizontal
                )

            if vehiculo.casillas[VEHICULO_FRENTE][desplazamientoHortizontal] < self.ancho - 1:
                casillaDelantera = (
                    vehiculo.casillas[VEHICULO_FRENTE][EJE_Y] +
                    desplazamientoVertical,
                    vehiculo.casillas[VEHICULO_FRENTE][EJE_X] +
                    desplazamientoHortizontal
                )

            # Todo: hacer un mapa de vehiculos en casilla, para indexar la buscqueda mas rapido
            # revisar si otro vehiculo ya ocupa la casilla
            for otroVehiculo in self.vehiculos:
                if casillaDelantera in otroVehiculo.casillas:
                    casillaDelantera = None
                if casillaTrasera in otroVehiculo.casillas:
                    casillaTrasera = None

            # Todo: se asume para la solucion inicial que el desplazamiento solo puede ser 1
            if casillaTrasera is not None:
                yield Movimiento(idVehiculo=vehiculo.id, inidiceVehiculo=indice, desplazamiento=-1)
            if casillaDelantera is not None:
                yield Movimiento(idVehiculo=vehiculo.id, inidiceVehiculo=indice, desplazamiento=1)
