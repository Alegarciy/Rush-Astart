# Importaciones de Archivo Tablero
from typing import List
from Tablero.cosntantes import EJE_X, EJE_Y, VEHICULO_ATRAS, VEHICULO_FRENTE
from Tablero.movimiento import Movimiento
from Tablero.vehiculo import Vehiculo
from Tablero.tablero import Tablero
from Algoritmos.algoritmos import aEstrella, getSolucionAEstrella
from Tablero.nodo import Nodo

# Importaciones de Archivo Lector
from AdministradorDeArchivos.adminsitradorDeArchivos import AdministradorDeArchivos

print('\n')

# PRUEBAS MOVIMIENTO
movimiento = Movimiento(0, 0, 5)
print('Movimento:')
print(f'idVehiculo [{movimiento.idVehiculo}],')
print(f'indiceVehiculo [{movimiento.inidiceVehiculo}],')
print(f'desplazamiento [{movimiento.desplazamiento}]')
print('\n')

# # PRUEBAS VEHICULO

# Vehiculo: creando vehiculos
vehiculo = Vehiculo(0, [[1, 3], [1, 4]], True)
camion = Vehiculo(1, [[1, 4], [1, 4], [1, 5]], True)

# Vehiculo: movimiento vehiculos
movimientoVehiculo = Movimiento(0, 0, 1)
movimientoCamion = Movimiento(0, 0, 4)


vehiculoActualizado = vehiculo.mover(movimientoVehiculo)
print(f'Vehiculo posicion inicial: {vehiculo.casillas}')
print(
    f'Vehiculo position despues de movimiento: {vehiculoActualizado.casillas}'
)

camionActualizado = camion.mover(movimientoCamion)
print(f'Vehiculo posicion inicial: {camion.casillas}')
print(
    f'Vehiculo position despues de movimiento: {camionActualizado.casillas}'
)
print('\n')

# Lector: generar tablero

print('Administrador de Archivos:')
tableroGenerado = AdministradorDeArchivos.leerArchivoConTablero(
    'Niveles/nivel1.csv'
)


for vehiculo in tableroGenerado.vehiculos:
    print(vehiculo)
print('\n')

# # Tablero: heuristica h^(x)

print('Herustica de completitud Hx:')
print(
    f'Casillas por cubrir de carro rojo: {tableroGenerado.getCasillasPorCubrir()}'
)

print('Vehiculos obstruyendo el paso:')
for vehiculoObstruyendo in tableroGenerado.getVehiculosObstruyendoPaso():
    print(f'Vehiculo Obstruyendo: {vehiculoObstruyendo}')
print('\n')

print('Casillas por cubrir por carro rojo:')
casillasPorCubrir = tableroGenerado.getCasillasPorCubrir()
print(f'Casillas: {casillasPorCubrir}')
print('\n')

print('Calcular el minimo de pasos para despejar ruta de rojo')
print(
    f'Minimo de pasos para despejar ruta: {tableroGenerado.MinimoDePasosParaDespejarPaso()}'
)

for movimeinto in tableroGenerado.getMovimientos():
    print(f'Movimiento: {movimeinto}')
print('\n')


# Pruebas exaustivas

print('Corrida de programa:')

print('Tablero not in:')
tableroGenerado3 = AdministradorDeArchivos.leerArchivoConTablero(
    'Niveles/nivel0.csv'
)

resultado = aEstrella(tableroGenerado3)
print('Prueba de rendimiento:')
print(f'Numero de nodos visitados: {resultado.numeroDeEstadosVisitados}')
print('\n')

print('Pasos de solucion')
pasosDeSolucion = getSolucionAEstrella(resultado)
numeroDePaso = 0

for paso in pasosDeSolucion:
    numeroDePaso += 1
    print(f'Numero de Paso {numeroDePaso}')
    print(paso)
    print()
