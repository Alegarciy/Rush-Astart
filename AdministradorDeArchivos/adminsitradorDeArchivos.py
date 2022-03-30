from csv import reader
from dataclasses import dataclass

from Tablero.tablero import Tablero


@dataclass(frozen=True)
class AdministradorDeArchivos:

    # El lector procesa el archivo y lo convierte en una instancia de tablero
    @staticmethod
    def leerArchivoConTablero(archivo: str) -> "Tablero":
        with open(archivo, "r") as archivoCSV:
            lectorCSV = reader(archivoCSV)
            # convierte a enteros los numeros procesados desde el lector CSV
            matriz = [[int(casilla) for casilla in fila] for fila in lectorCSV]
            return Tablero.generarTableroDeMatriz(matriz)
