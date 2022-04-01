from typing import Tuple
import pygame
from AdministradorDeArchivos.adminsitradorDeArchivos import AdministradorDeArchivos
from Tablero.vehiculo import Vehiculo
from Algoritmos.algoritmos import aEstrella, getSolucionAEstrella

global coloresDeAutos
coloresDeAutos = {
    0: (193, 11, 41),
    1: (193, 11, 123),
    2: (184, 11, 193),
    3: (93, 11, 193),
    4: (41, 11, 193),
    5: (11, 87, 193),
    6: (11, 178, 193),
    7: (11, 193, 163),
    8: (11, 193, 81),
    9: (78, 193, 11),
    10: (166, 193, 11),
    11: (193, 130, 11),
    12: (214, 145, 146),
    13: (214, 145, 209),
    14: (157, 145, 214),
    15: (145, 194, 214),
    16: (145, 214, 166),
    17: (187, 214, 145),
    18: (214, 176, 145)
}


def grid(ventana, tamano, numeroDeFilas, vehiculosRecibidos):
    # este algoritmo recibe un resultado del algoritmo
    distanciaEntreFilas = tamano // numeroDeFilas
    x = 0
    y = 0
    for linea in range(numeroDeFilas):
        x += distanciaEntreFilas
        y += distanciaEntreFilas
        pygame.draw.line(ventana, (0, 0, 0), (x, 0), (x, tamano))
        pygame.draw.line(ventana, (0, 0, 0), (0, y), (tamano, y))

    pintarCarros(ventana, vehiculosRecibidos, distanciaEntreFilas)


def generarCuadradoEnGrid(ventana, numeroDeColumna, numeroDeFila, color, tamano):
    pygame.draw.rect(ventana, color, pygame.Rect(
        numeroDeFila*tamano, numeroDeColumna*tamano, tamano, tamano))
    pygame.display.flip()


def pintarCarros(ventana, vehiculos: Tuple[Vehiculo], tamano):
    # pinta la grid con los autos
    for vehiculo in vehiculos:
        for casilla in vehiculo.casillas:
            generarCuadradoEnGrid(
                ventana, casilla[0], casilla[1], coloresDeAutos.get(vehiculo.id), tamano)


def redraw(ventana):
    global tamano, numeroDeFilas
    # Llenar una ventana con color negro
    ventana.fill((76, 139, 191))
    pygame.draw.rect(ventana, (255, 255, 255),
                     pygame.Rect(0, 0, tamano, tamano))


def mostrarResultadosTexto(resultado):
    font1 = pygame.font.SysFont('freesanbold.ttf', 50)
    text1 = font1.render('GeeksForGeeks', True, (0, 255, 0))
    textRect1 = text1.get_rect()
    textRect1.center = (250, 250)
    return


def desplegarTexto(ventana, texto, x, y):
    font1 = pygame.font.SysFont('arial', 20)
    text1 = font1.render(texto, True, (255, 255, 255))
    ventana.blit(text1, (x, y))
    pygame.display.update()


def main():
    global tamano, numeroDeFilas
    tamano = 500
    numeroDeFilas = 6
    contador = 0

    pygame.font.init()
    pygame.font.get_init()

    # Llama al solver del algoritmo
    # Todo: implementar un lector de archivos
    tableroGenerado = AdministradorDeArchivos.leerArchivoConTablero(
        'Niveles/nivel1.csv'
    )

    resultado = aEstrella(tableroGenerado)
    pasosDeSolucion = getSolucionAEstrella(resultado)

    ventana = pygame.display.set_mode((tamano + 250, tamano))
    ventana.fill((76, 139, 191))
    pygame.draw.rect(ventana, (255, 255, 255),
                     pygame.Rect(0, 0, tamano, tamano))

    grid(ventana, tamano, numeroDeFilas, pasosDeSolucion[contador])

    seguirJugando = True
    print(pygame.font.get_fonts())

    # Crear texto

    # Loop principal del juego
    while seguirJugando:
        # Event Listener del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    if contador < len(pasosDeSolucion) - 1:
                        contador += 1
                        grid(ventana, tamano, numeroDeFilas,
                             pasosDeSolucion[contador])
                        pygame.display.update()
                        desplegarTexto(ventana, "# de Paso", tamano, 0)
                        desplegarTexto(ventana, str(contador), tamano, 25)
                        desplegarTexto(
                            ventana, "# de Nodos Recorridos", tamano, 100)
                        desplegarTexto(ventana, str(
                            resultado.numeroDeEstadosVisitados), tamano, 125)
                        print('Tecla derecha')
                if evento.key == pygame.K_LEFT:
                    if contador > 0:
                        contador -= 1
                        grid(ventana, tamano, numeroDeFilas,
                             pasosDeSolucion[contador])
                        pygame.display.update()
                        desplegarTexto(ventana, "# de Paso", tamano, 0)
                        desplegarTexto(ventana, str(contador), tamano, 50)
                        print('Tecla izquieda')

        redraw(ventana)


main()
