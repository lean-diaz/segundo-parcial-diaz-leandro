# Importamos Pygame y las funciones
import pygame
from funciones import *  # Asegúrate de que funciones.py contiene las funciones necesarias como generar_tablero_con_naves.

# Configuramos la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Batalla Naval")
pygame.init()

# Colores y configuraciones gráficas
COLOR_AGUA = (0, 128, 255)  # Azul
COLOR_NAVE = (255, 0, 0)  # Rojo
COLOR_BOTON = (0, 128, 255)  # Azul Claro
COLOR_TEXTO = (255, 255, 255)  # Blanco
TAMANIO_CASILLA = 50
MARGEN_TABLERO = 100
fuente = pygame.font.SysFont("Arial", 30)

# Imagen de fondo
imagen_fondo = pygame.image.load("img/fondo.jpeg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Botones
botones = {
    "nivel": pygame.Rect(300, 200, 200, 50),
    "jugar": pygame.Rect(300, 270, 200, 50),
    "puntajes": pygame.Rect(300, 340, 200, 50),
    "salir": pygame.Rect(300, 410, 200, 50),
    "reiniciar": pygame.Rect(700, 200, 100, 50),
    "volver": pygame.Rect(700, 270, 100, 50)
}

# Variables de estado
menu_activo = True
juego_activo = False
mostrar_reiniciar = False
mostrar_volver = False
puntajes_json = "puntajes.json"
corriendo = True
tablero = None
disparos_realizados = []
puntaje = 0

# Bucle principal del juego
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Menú principal
            if menu_activo:
                # Boton Nivel
                if botones["nivel"].collidepoint((mouse_x, mouse_y)):
                    print("Se presionó 'Nivel'")
                # Boton Jugar
                elif botones["jugar"].collidepoint((mouse_x, mouse_y)):
                    # Ocultar menú y solicitar nickname
                    menu_activo = False
                    juego_activo = False
                    mostrar_reiniciar = False
                    mostrar_volver = False
            
                    # Solicitar nickname
                    nickname = pedir_nickname()

                    # Inicializar tablero y juego
                    tablero = generar_tablero_con_naves()
                    menu_activo = False
                    juego_activo = True
                    mostrar_reiniciar = True
                    mostrar_volver = True
                    puntaje = 0  # Puntaje inicial
                    print(f"Se presionó 'Jugar'. Nickname: {nickname}")

                # Botón Ver Puntajes
                elif botones["puntajes"].collidepoint((mouse_x, mouse_y)):
                    print("Se presionó 'Ver Puntajes'")
    
                    # Obtener y mostrar los tres mejores puntajes
                    mejores_puntajes = obtener_mejores_puntajes(puntajes_json)
    
                    print("Los tres mejores puntajes son:")
    
                    for i in range(len(mejores_puntajes)):
                        print(f"{i + 1}. Nick: {mejores_puntajes[i]['nickname']}, Puntaje: {mejores_puntajes[i]['puntaje']}")
                    
                    
                # Boton Salir
                elif botones["salir"].collidepoint((mouse_x, mouse_y)):
                    corriendo = False
                    print("Se presionó 'Salir'")
            
            # Validaciones durante el juego
            elif juego_activo:
                # Boton Reiniciar
                if botones["reiniciar"].collidepoint((mouse_x, mouse_y)):
                    tablero = generar_tablero_con_naves()
                    disparos_realizados.clear()
                    puntaje = 0
                    print("Se presionó 'Reiniciar'")
                
                # Boton Volver
                elif botones["volver"].collidepoint((mouse_x, mouse_y)):
                    # Guardar puntaje antes de reiniciar
                    guardar_puntaje("puntajes.json", nickname, puntaje)

                    # Reiniciar estado del menú
                    menu_activo = True
                    juego_activo = False
                    mostrar_reiniciar = False
                    mostrar_volver = False
                    tablero = None
                    disparos_realizados.clear()
                    puntaje = 0
                    print("Se presionó 'Volver'")

                # Disparos en el tablero
                else:
                    # Calcular la columna y fila a partir de la posición del mouse
                    columna = (mouse_x - MARGEN_TABLERO) // TAMANIO_CASILLA
                    fila = (mouse_y - MARGEN_TABLERO) // TAMANIO_CASILLA

                    # Verificar si la fila y columna están dentro de los límites del tablero
                    fila_valida = 0 <= fila < 10
                    columna_valida = 0 <= columna < 10
                    tablero_existe = tablero is not None

                    if fila_valida and columna_valida and tablero_existe:
                        # Crear un disparo como una tupla (fila, columna)
                        disparo = (fila, columna)

                        # Verificar si ya se ha disparado en esta posición
                        ya_disparo = disparo in disparos_realizados
                        if ya_disparo:
                            print("Ya disparaste aquí.")
                        else:
                            # Agregar el disparo a la lista de disparos realizados
                            disparos_realizados.append(disparo)

                            # Comprobar si el disparo fue un impacto
                            es_impacto = tablero[fila][columna] == 1
                            if es_impacto:
                                print("¡Impacto!")
                                puntaje += 5
                                partes_hundidas = verificar_hundimiento(tablero, fila, columna)
                                if partes_hundidas > 0:
                                    puntaje += partes_hundidas * 10  # Sumar puntos por cada parte hundida
                            else:
                                print("Agua.")
                                puntaje -= 1

    # Dibujar pantalla
    pantalla.blit(imagen_fondo, (0, 0))

    if menu_activo:  # Dibujar menú principal
        for boton in ["nivel", "jugar", "puntajes", "salir"]:
            pygame.draw.rect(pantalla, COLOR_BOTON, botones[boton])
            texto_boton = fuente.render(boton.capitalize(), True, COLOR_TEXTO)
            rect_texto = texto_boton.get_rect(center=botones[boton].center)
            pantalla.blit(texto_boton, rect_texto)

    elif juego_activo:  # Dibujar el juego
        if tablero:
            for fila in range(len(tablero)):
                for columna in range(len(tablero[fila])):
                    x = MARGEN_TABLERO + columna * TAMANIO_CASILLA
                    y = MARGEN_TABLERO + fila * TAMANIO_CASILLA
                
                    # Determinar el color basado en el estado del disparo
                    if (fila, columna) in disparos_realizados:
                        color = (255, 255, 0)  # Color para casillas disparadas
                    else:
                        if tablero[fila][columna] == 0:
                            color = COLOR_AGUA  # Agua
                        else:
                            color = COLOR_NAVE  # Nave

                    pygame.draw.rect(pantalla, color, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))
                    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 2)

            # Mostrar puntaje en pantalla
            texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, COLOR_TEXTO)
            pantalla.blit(texto_puntaje, (10, 10))

            # Dibujar botones adicionales si están visibles
            if mostrar_reiniciar:
                pygame.draw.rect(pantalla, COLOR_BOTON, botones["reiniciar"])
                texto_reiniciar = fuente.render("Reiniciar", True, COLOR_TEXTO)
                rect_reiniciar = texto_reiniciar.get_rect(center=botones["reiniciar"].center)
                pantalla.blit(texto_reiniciar, rect_reiniciar)

            if mostrar_volver:
                pygame.draw.rect(pantalla, COLOR_BOTON, botones["volver"])
                texto_volver = fuente.render("Volver", True, COLOR_TEXTO)
                rect_volver = texto_volver.get_rect(center=botones["volver"].center)
                pantalla.blit(texto_volver, rect_volver)



    pygame.display.flip()

pygame.quit()
