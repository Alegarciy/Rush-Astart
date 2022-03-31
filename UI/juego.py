import pygame

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


def grid(ventana, tamano, numeroDeFilas):
    distanciaEntreFilas = tamano // numeroDeFilas
    x = 0
    y = 0
    for linea in range(numeroDeFilas):
        x += distanciaEntreFilas
        y += distanciaEntreFilas
        pygame.draw.line(ventana, (0, 0, 0), (x, 0), (x, tamano))
        pygame.draw.line(ventana, (0, 0, 0), (0, y), (tamano, y))

    generarCuadradoEnGrid(
        ventana, 2, 2, coloresDeAutos.get(3), distanciaEntreFilas)
    generarCuadradoEnGrid(
        ventana, 4, 2, coloresDeAutos.get(4), distanciaEntreFilas)


def generarCuadradoEnGrid(ventana, numeroDeColumna, numeroDeFila, color, tamano):
    pygame.draw.rect(ventana, color, pygame.Rect(
        numeroDeFila*tamano, numeroDeColumna*tamano, tamano, tamano))
    pygame.display.flip()


def redraw(ventana):
    global tamano, numeroDeFilas
    # Llenar una ventana con color negro
    ventana.fill((255, 255, 255))


def main():
    global tamano, numeroDeFilas
    tamano = 500
    numeroDeFilas = 6

    ventana = pygame.display.set_mode((tamano, tamano))
    ventana.fill((255, 255, 255))
    grid(ventana, tamano, numeroDeFilas)
    pygame.display.update()

    seguirJugando = True

    # Loop principal del juego
    while seguirJugando:
        # Event Listener del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()

        redraw(ventana)


main()
