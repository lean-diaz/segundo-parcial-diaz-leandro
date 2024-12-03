# Importamos Pygame y las funciones
import pygame
from funciones import *

# Configuramos la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Batalla Naval")
pygame.init()

# Colores
COLOR_AGUA = (0, 128, 255)  # Azul, para el agua
COLOR_NAVE_OCULTA = (0, 128, 255)  # Azul (mismo que agua para ocultar)
COLOR_NAVE_DESCUBIERTA = (255, 0, 0)  # Rojo, para la nave descubierta
COLOR_BOTON = (0, 128, 255)  # Azul Claro, para los botones
COLOR_TEXTO = (255, 255, 255)  # Blanco, usado para texto

# Configuraciones del tablero y fuente de texto
TAMANIO_CASILLA = 50 # Tamaño de cada casilla del tablero
MARGEN_TABLERO = 100 # Margen desde la esquina superior izquierda
fuente = pygame.font.SysFont("Arial", 30) # Fuente para mostrar texto

# Cargamos y escalamos la imagen de fondo para ajustarla a la pantalla
imagen_fondo = pygame.image.load("Segundo_Parcial_final/img/fondo.jpeg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Creamos un diccionario que contiene los botones con sus posiciones y dimensiones
botones = {
    "nivel": pygame.Rect(300, 200, 200, 50),
    "jugar": pygame.Rect(300, 270, 200, 50),
    "puntajes": pygame.Rect(300, 340, 200, 50),
    "salir": pygame.Rect(300, 410, 200, 50),
    "reiniciar": pygame.Rect(700, 200, 100, 50),
    "volver": pygame.Rect(700, 270, 100, 50)
}

# Variables de estado para controlar el flujo del juego
menu_activo = True # Indica si el menú principal está activo
juego_activo = False # Indica si el juego está en progreso
mostrar_reiniciar = False # Indica si el botón 'Reiniciar' debe mostrarse
mostrar_volver = False # Indica si el botón 'Volver' debe mostrarse
puntajes_json = "puntajes.json" # Ruta al archivo donde se almacenan los puntajes
corriendo = True # Controla el bucle principal del juego
tablero = None # Representación del tablero (matriz)
disparos_realizados = [] # Lista de disparos realizados por el jugador

# Inicializamos el estado de las casillas
estado_casillas = inicializar_estado_casillas()

puntaje = 0 # Puntaje inicial del jugador

# Bucle principal del juego
while corriendo:
    # Iteramos sobre los eventos de Pygame
    for evento in pygame.event.get():
        # Si el evento es salir de la ventana
        if evento.type == pygame.QUIT:
            corriendo = False # Finalizamos el bucle
        
        # Detectamos clicks del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtenemos las posiciones (x, y) del mouse
            mouse_posiciones = pygame.mouse.get_pos() 
            mouse_x = mouse_posiciones[0]
            mouse_y = mouse_posiciones[1]

            # Menú principal
            # Si el menu principal está activo ... 
            if menu_activo:
                # Verificamos si se presionó un boton del menu
                if botones["nivel"].collidepoint((mouse_x, mouse_y)): # Boton Nivel
                    print("Se presionó 'Nivel'")
                
                elif botones["jugar"].collidepoint((mouse_x, mouse_y)): # Boton Jugar
                    # Ocultar menú y solicitar nickname
                    menu_activo = False # Ocultamos el menu principal
                    juego_activo = False # Activamos el juego
                    
                    # Inicializamos el tablero y las variables del juego
                    mostrar_reiniciar = False # Desactivamos la visualizacion del menu principal
                    mostrar_volver = False # Ocultamos el boton de volver temporalmente

                    # Solicitar nickname
                    nickname = pedir_nickname() # Llamamos a la funcion para pedir el nombre del jugador

                    # Inicializar tablero y juego
                    tablero = generar_tablero_con_naves() # Generamos un tablero con naves ubicadas aleatoriamente
                    
                    # Inicializamos el estado de las casillas
                    estado_casillas = inicializar_estado_casillas()
                    
                    # Cambiar estados para activar el juego
                    menu_activo = False # Desactivamos el menu principal
                    juego_activo = True # Activamos el estado de juego
                    mostrar_reiniciar = True # Activamos el boton de reiniciar 
                    mostrar_volver = True # Activamos el boton de voler 
                    puntaje = 0  # Puntaje inicializado en 0
                    disparos_realizados.clear() # Limpiamos la lista de disparos realizados
                    print(f"Se presionó 'Jugar'. Nickname: {nickname}") # Notifica que se inició el juego con el nickname dado
                
                elif botones["puntajes"].collidepoint((mouse_x, mouse_y)): # Botón Ver Puntajes
                    print("Se presionó 'Ver Puntajes'")

                    # Obtener y mostrar los tres mejores puntajes
                    mejores_puntajes = obtener_mejores_puntajes(puntajes_json) # Llama a una función para obtener los puntajes

                    print("Los tres mejores puntajes son:")

                    # Iteramos sobre los puntajes obtenidos
                    for i in range(len(mejores_puntajes)):
                        # Imprimimos el ranking con la posicion y detalles del puntaje
                        print(f"{i + 1}. Nick: {mejores_puntajes[i]['nickname']}, Puntaje: {mejores_puntajes[i]['puntaje']}")

                elif botones["salir"].collidepoint((mouse_x, mouse_y)): # Boton Salir
                    corriendo = False # Finalizamos el bucle
                    print("Se presionó 'Salir'")

            # Validaciones durante el juego
            elif juego_activo: # Solo procesamos estas acciones si el juego está activo
                
                if botones["reiniciar"].collidepoint((mouse_x, mouse_y)): # Boton Reiniciar
                    tablero = generar_tablero_con_naves() # Generamos un nuevo tablero con las naves reposicionadas
                    
                    # Inicializamos el estado de las casillas
                    estado_casillas = inicializar_estado_casillas()
                    
                    disparos_realizados.clear() # Limpiamos la lista de disparos realizados
                    puntaje = 0 # Reiniciamos el puntaje a 0
                    print("Se presionó 'Reiniciar'") # Notificamos que el boton fue presionado
                
                elif botones["volver"].collidepoint((mouse_x, mouse_y)): # Boton Volver
                    guardar_puntaje("puntajes.json", nickname, puntaje) # Guarda el puntaje actual en un archivo JSON

                    # Reiniciamos estado del menú
                    menu_activo = True # Activamos el menu principal
                    juego_activo = False # Desactivamos el juego
                    mostrar_reiniciar = False # Ocultamos el boton de reiniciar
                    mostrar_volver = False # Ocultamos el boton de volver
                    tablero = None # Limpia el tablero
                    estado_casillas = None # Limpiamos el estado de las casillas
                    disparos_realizados.clear() # Limpia la lista de disparos realizados
                    puntaje = 0 # Reiniciamos el puntaje
                    print("Se presionó 'Volver'")

                # Disparos en el tablero
                else:
                    # Calcular la columna y fila a partir de la posición del mouse
                    columna = (mouse_x - MARGEN_TABLERO) // TAMANIO_CASILLA # Determina la columna clicada
                    fila = (mouse_y - MARGEN_TABLERO) // TAMANIO_CASILLA # Determina la fila clicada

                    # Verificar si la fila está dentro de los límites del tablero
                    fila_valida = False # Bandera inicial para la validez de la fila
                    if 0 <= fila < 10: # Comprueba si la fila está en el rango válido
                        fila_valida = True

                    # Verificar si la columna está dentro de los límites del tablero
                    columna_valida = False # Bandera inicial para la validez de la columna
                    if 0 <= columna < 10: # Comprueba si la columna está en el rango válido
                        columna_valida = True
                    
                    # Verificar si el tablero existe
                    tablero_existe = False # Bandera inicial para la existencia del tablero
                    if tablero is not None: # Comprueba si el tablero está definido
                        tablero_existe = True
                    
                    # Proceder solo si fila, columna y tablero son válidos
                    if fila_valida and columna_valida and tablero_existe: # Nos aseguramos de que todo sea válido antes de continuar
                        # Crear un disparo como una tupla (fila, columna)
                        disparo = None # Inicializamos la variable del disparo
                        disparo_fila = fila # Guardamos la fila del disparo
                        disparo_columna = columna # Guardamos la columna del disparo
                        disparo = (disparo_fila, disparo_columna) # Creamos el disparo como una tupla (fila, columna)

                        # Verificar si ya se ha disparado en esta posición
                        ya_disparo = False # Bandera inicial para verificar disparos repetidos
                        if disparo in disparos_realizados: # Comprueba si la posición ya fue disparada
                            ya_disparo = True
                        
                        if ya_disparo: # Si ya se disparó en esta posición
                            print("Ya disparaste aquí.")
                        else:
                            # Marcar la casilla como disparada
                            estado_casillas[fila][columna] = True # Actualiza el estado de la casilla

                            disparos_realizados.append(disparo) # Agregar el disparo a la lista de disparos realizados
                        
                            # Comprobar si el disparo fue un impacto
                            es_impacto = False # Bandera inicial para verificar impactos
                            if tablero[fila][columna] == 1: # Verifica si en la posición disparada hay una parte de nave
                                es_impacto = True
                            
                            if es_impacto: # Si hubo un impacto
                                print("¡Impacto!")
                                puntaje += 5 # Incrementa el puntaje por un impacto

                                # Verificar cuántas partes se hundieron
                                partes_hundidas = verificar_hundimiento(tablero, fila, columna) # Comprueba si se hundió una nave
                                # Si al menos una parte se hundió
                                if partes_hundidas > 0:
                                    puntaje += partes_hundidas * 10  # Sumar puntos por cada parte hundida
                            # Si no hubo impacto
                            else:
                                print("Agua.")
                                puntaje -= 1 # Restamos 1 punto

    # Dibujar pantalla
    pantalla.blit(imagen_fondo, (0, 0))

    # Dibujar menú principal
    if menu_activo:
        # Iteramos sobre los nombres de los botones del menú
        for boton in ["nivel", "jugar", "puntajes", "salir"]:
            pygame.draw.rect(pantalla, COLOR_BOTON, botones[boton]) # Dibuja un rectángulo para el botón actual
            texto_boton = fuente.render(boton.capitalize(), True, COLOR_TEXTO) # Renderiza el texto del botón
            rect_texto = texto_boton.get_rect(center=botones[boton].center) # Centra el texto dentro del botón
            pantalla.blit(texto_boton, rect_texto) # Dibuja el texto sobre el botón

    # Si el juego está activo, dibujamos los elementos del juego
    elif juego_activo: 
        # Aseguramos que el tablero y el estado de las casillas existan
        if tablero and estado_casillas:
            # Iteramos por cada fila del tablero
            for fila in range(len(tablero)):
                # Iteramos por cada columna en la fila
                for columna in range(len(tablero[fila])):
                    # Calculamos la posición (x, y) de la casilla actual en la pantalla
                    x = MARGEN_TABLERO + columna * TAMANIO_CASILLA
                    y = MARGEN_TABLERO + fila * TAMANIO_CASILLA
                
                    # Determinar el color basado en el estado del disparo
                    # Si esta casilla ya fue disparada
                    if estado_casillas[fila][columna]: 
                        # Si hay una nave en esta posición
                        if tablero[fila][columna] == 1:
                            color = COLOR_NAVE_DESCUBIERTA  # Rojo para nave descubierta
                        else:
                            color = (255, 255, 0)  # Amarillo para agua
                    else:
                        color = COLOR_NAVE_OCULTA  # Azul para casillas no descubiertas
                    
                    # Dibuja el rectángulo que representa la casilla en la pantalla
                    pygame.draw.rect(pantalla, color, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))
                    # Dibuja un borde negro alrededor de la casilla
                    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 2)

            # Mostrar puntaje en pantalla
            texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, COLOR_TEXTO)
            pantalla.blit(texto_puntaje, (10, 10))

            # Dibujar botones adicionales si están visibles
            if mostrar_reiniciar:
                pygame.draw.rect(pantalla, COLOR_BOTON, botones["reiniciar"]) # Dibuja el botón
                texto_reiniciar = fuente.render("Reiniciar", True, COLOR_TEXTO) # Renderiza el texto del botón
                rect_reiniciar = texto_reiniciar.get_rect(center=botones["reiniciar"].center) # Centra el texto
                pantalla.blit(texto_reiniciar, rect_reiniciar) # Dibuja el texto en el botón

            if mostrar_volver:
                pygame.draw.rect(pantalla, COLOR_BOTON, botones["volver"]) # Dibuja el botón
                texto_volver = fuente.render("Volver", True, COLOR_TEXTO) # Renderiza el texto del botón
                rect_volver = texto_volver.get_rect(center=botones["volver"].center) # Centra el texto
                pantalla.blit(texto_volver, rect_volver) # Dibuja el texto en el botón

    pygame.display.flip()

pygame.quit()