from typing import Tuple
from unittest import result
import pygame
from Tablero.vehiculo import Vehiculo
from AdministradorDeArchivos.adminsitradorDeArchivos import AdministradorDeArchivos
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

WHITE = (255, 255, 255)
BLACK = (0,  0,  0)

RED = (255, 87, 87)
GREEN = (0, 255,  0)

YELLOW = (255, 222, 89)


def grid(ventana, tamano, numeroDeFilas, vehiculosRecibidos):
    # este algoritmo recibe un resultado del algoritmo
    pygame.draw.rect(ventana, (255, 255, 255),
                     pygame.Rect(0, 0, tamano, tamano))
    distanciaEntreFilas = tamano // numeroDeFilas
    x = 0
    y = 0
    for linea in range(numeroDeFilas):
        x += distanciaEntreFilas
        y += distanciaEntreFilas
        pygame.draw.line(ventana, (0, 0, 0), (x, 0), (x, tamano))
        pygame.draw.line(ventana, (0, 0, 0), (0, y), (tamano, y))

    pintarCarros(ventana, vehiculosRecibidos, distanciaEntreFilas)


def pintarCarros(ventana, vehiculos: Tuple[Vehiculo], tamano):
    # pinta la grid con los autos
    for vehiculo in vehiculos:
        for casilla in vehiculo.casillas:
            generarCuadradoEnGrid(
                ventana, casilla[0], casilla[1], coloresDeAutos.get(vehiculo.id), tamano)


def generarCuadradoEnGrid(ventana, numeroDeColumna, numeroDeFila, color, tamano):
    pygame.draw.rect(ventana, color, pygame.Rect(
        numeroDeFila*tamano, numeroDeColumna*tamano, tamano, tamano))
    pygame.display.flip()


def redraw(ventana):
    global tamano, numeroDeFilas
    # Llenar una ventana con color negro
    ventana.fill((255, 255, 255))


def button_create(text, rect, inactive_color, active_color, action):

    font = pygame.font.Font(None, 40)

    button_rect = pygame.Rect(rect)

    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)

    return [text, text_rect, button_rect, inactive_color, active_color, action, False]


def button_check(info, event):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if event.type == pygame.MOUSEMOTION:
        # hover = True/False
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()


def button_draw(screen, info):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)


def getPasosResultado(nombreArchivo):
    try:
        tableroGenerado = AdministradorDeArchivos.leerArchivoConTablero(
            nombreArchivo
        )
        return aEstrella(tableroGenerado)
    except:
        tableroGenerado = AdministradorDeArchivos.leerArchivoConTablero(
            'Niveles/nivel0.csv'
        )
        return aEstrella(tableroGenerado)


def desplegarTexto(ventana, texto, x, y):
    font1 = pygame.font.SysFont('arial', 20)
    text1 = font1.render(texto, True, (255, 255, 255))
    ventana.blit(text1, (x, y))
    pygame.display.update()


def desplegarContador(ventana, tamano, contador, resultado):
    desplegarTexto(ventana, "# de Paso", tamano, 0)
    desplegarTexto(ventana, str(contador), tamano, 25)
    desplegarTexto(
        ventana, "# de Nodos Recorridos", tamano, 100)
    desplegarTexto(ventana, str(
        resultado.numeroDeEstadosVisitados), tamano, 125)


def game():

    global tamano, numeroDeFilas, seguirJugando
    tamano = 500
    numeroDeFilas = 6
    contador = 0

    # Initialize font method
    pygame.font.init()
    pygame.font.get_init()

    ventana = pygame.display.set_mode((tamano + 200, 650))
    ventana.fill((255, 255, 255))

    # Llama al solver del algoritmo
    # Todo: nivel que carga por default
    tableroGenerado = AdministradorDeArchivos.leerArchivoConTablero(
        'Niveles/nivel0.csv'
    )
    resultado = aEstrella(tableroGenerado)
    pasosDeSolucion = getSolucionAEstrella(resultado)
    grid(ventana, tamano, numeroDeFilas, pasosDeSolucion[contador])

    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(55, 540, 200, 40)
    color_inactive = (71, 71, 71)
    color_active = (20, 20, 20)
    color = color_inactive
    active = False
    text = ''

    button_return = button_create(
        "RETURN", (150, 590, 200, 40), RED, YELLOW, on_click_button_return)

    pygame.display.update()
    seguirJugando = True

    # Loop principal del juego
    while seguirJugando:
        # Event Listener del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(evento.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    if contador < len(pasosDeSolucion) - 1:
                        contador += 1
                        grid(ventana, tamano, numeroDeFilas,
                             pasosDeSolucion[contador])
                elif evento.key == pygame.K_LEFT:
                    if contador > 0:
                        contador -= 1
                        grid(ventana, tamano, numeroDeFilas,
                             pasosDeSolucion[contador])
                elif active:
                    if evento.key == pygame.K_RETURN:
                        pygame.draw.rect(ventana, (255, 255, 255),
                                         pygame.Rect(0, 500, tamano, tamano))
                        contador = 0
                        resultado = getPasosResultado(
                            'Niveles/' + text + '.csv')
                        pasosDeSolucion = getSolucionAEstrella(resultado)
                        grid(ventana, tamano, numeroDeFilas,
                             pasosDeSolucion[contador])
                        text = ''
                    elif evento.key == pygame.K_BACKSPACE:
                        pygame.draw.rect(ventana, (255, 255, 255),
                                         pygame.Rect(0, 500, tamano, tamano))
                        text = text[:-1]

                    else:
                        text += evento.unicode

        #ventana.fill((30, 30, 30))
        # Render the current text.

        txt_label = font.render("Select the file here:", 1, (71, 71, 71))
        ventana.blit(txt_label, (55, 515))
        pygame.draw.rect(ventana, (255, 255, 255),
                         pygame.Rect(500, 0, tamano, tamano))
        txt_pasos = font.render("Pasos: " + str(contador), 1, (71, 71, 71))
        ventana.blit(txt_pasos, (500, 0))
        txt_nodos = font.render(
            "Nodos Recorridos: ", 1, (71, 71, 71))
        ventana.blit(txt_nodos, (500, 50))
        txt_cantidadNodo = font.render(
            str(resultado.numeroDeEstadosVisitados), 1, (71, 71, 71))
        ventana.blit(txt_cantidadNodo, (500, 75))
        txt_box = font.render(text, True, color)
        # Resize the box if the text is too long.

        width = max(400, txt_box.get_width()+10)
        input_box.w = width
        # Blit the text.
        ventana.blit(txt_box, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(ventana, color, input_box, 2)
        #grid(ventana, tamano, numeroDeFilas)

        button_check(button_return, evento)
        button_draw(ventana, button_return)

        clock.tick(30)

        pygame.display.flip()

        # redraw(ventana)
    # para tomar el nombre del file es text
    # print(text)


def on_click_button_1():
    print('You clicked Button 1')
    game()


def on_click_button_3():
    print('You exited the game')
    global running, seguirJugando
    running = False
    seguirJugando = False


def on_click_button_return():
    print('You clicked Button Return')
    main()


def main():
    global running
    running = True
    ventana = pygame.display.set_mode((500, 650))
    ventana.fill((255, 255, 255))

    button_1 = button_create(
        "START", (150, 275, 200, 100), RED, YELLOW, on_click_button_1)
    button_3 = button_create("EXIT", (150, 425, 200, 100),
                             RED, YELLOW, on_click_button_3)

    background = pygame.image.load("UI/background.png")

    while running:

        # - events -

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            button_check(button_1, event)
            button_check(button_3, event)
            #    pass

        ventana.fill(BLACK)
        ventana.blit(background, (0, 0))
        button_draw(ventana, button_1)
        button_draw(ventana, button_3)

        pygame.display.update()


pygame.init()
main()
pygame.quit()
