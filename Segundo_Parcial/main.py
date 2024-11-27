# Importamos Pygame y las funciones
import pygame
from funciones import *

# Configuramos la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
# Titulo de la ventana
pygame.display.set_caption("Batalla Naval")
# Inicializamos Pygame
pygame.init()

# Colores y configuraciones gráficas
COLOR_AGUA = (0,128,255) # Azul
COLOR_NAVE = (255, 0, 0) # Rojo
COLOR_BOTON = (0, 128, 255) # Azul Claro
COLOR_TEXTO = (255, 255, 255) # Blanco
TAMANIO_CASILLA = 50 # Tamaño para cada casiila del tablero
MARGEN_TABLERO = 100 # Margen para posicionar el tablero
fuente = pygame.font.SysFont("Arial", 30) # Fuente de texto

# Cargamos la imagen de fondo
imagen_fondo = pygame.image.load("img/fondo.jpeg")
# Ajustamos la imagen al tamaño de la ventana
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Creamos un diccionario con los botones como rectangulos
botones = {
    "nivel": pygame.Rect(300,200,200,50),
    "jugar": pygame.Rect(300,270,200,50),
    "puntajes": pygame.Rect(300,340,200,50),
    "salir": pygame.Rect(300,410,200,50),
    "reiniciar": pygame.Rect(700,200,100,50)
}

menu_activo = True # Controlamos cuando se visualiza el menu principal
mostrar_reiniciar = False # Controlamos si el boton Reiniciar está visible
corriendo = True # Controlamos el bucle del juego
tablero = None # Contiene el tablero generado

# Bucle principal del juego
while corriendo:
    # Capturamos eventos del sistema
    for evento in pygame.event.get():
        # Si el usuario cierra la ventana
        if evento.type == pygame.QUIT:
            corriendo = False # Salimos del bucle
        
        # Si el usuario hace clic con el mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Coordenadas del clic (x, y)
            mouse_pos = pygame.mouse.get_pos() 
            mouse_x = mouse_pos[0] # Coordenada x del clic
            mouse_y = mouse_pos[1] # Coordenada y del clic

            if menu_activo:
                # Verificamos en que boton se hizo clic
                if botones["nivel"].collidepoint((mouse_x, mouse_y)):
                    print("Se presionó 'Nivel'")
            
                elif botones["jugar"].collidepoint((mouse_x, mouse_y)):
                    tablero = generar_tablero_con_naves()
                    mostrar_reiniciar = True
                    menu_activo = False
                    print("Se presionó 'Jugar'")
            
                elif botones["puntajes"].collidepoint((mouse_x, mouse_y)):
                    print("Se presionó 'Ver Puntajes'")
            
                elif botones["salir"].collidepoint((mouse_x, mouse_y)):
                    print("Se presionó 'Salir'")
                    corriendo = False
            
            # Interacción con el botón "Reiniciar"
            if mostrar_reiniciar and botones["reiniciar"].collidepoint((mouse_x, mouse_y)):
                tablero = generar_tablero_con_naves()
                print("Se presionó 'Reiniciar'")
    
    # Dibujamos la pantalla
    pantalla.blit(imagen_fondo, (0, 0))
    
    # Dibujamos los botones
    for boton in botones: # Iteramos sobre las claves del diccionario
        
        # Dibujamos los botones del menú solo si está activo
        if menu_activo and boton != "reiniciar":
            pygame.draw.rect(pantalla, COLOR_BOTON, botones[boton])
            texto = fuente.render(boton.capitalize(), True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=botones[boton].center)
            pantalla.blit(texto, texto_rect)

        # Dibujamos el botón "Reiniciar" si debe mostrarse
        if boton == "reiniciar" and mostrar_reiniciar:
            pygame.draw.rect(pantalla, COLOR_BOTON, botones["reiniciar"])
            texto = fuente.render("Reiniciar", True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=botones["reiniciar"].center)
            pantalla.blit(texto, texto_rect)

    # Dibujamos el tablero si se ganará
    if tablero:
        # Obtenemos los datos del tablero para dibujarlo
        datos_tablero = obtener_datos_tablero(tablero)

        for casilla in datos_tablero:
            fila = casilla['fila']
            columna = casilla['columna']
            estado = casilla['estado']
            
            # Calcular la posición de la casilla en pantalla
            x = MARGEN_TABLERO + columna * TAMANIO_CASILLA
            y = MARGEN_TABLERO + fila * TAMANIO_CASILLA
            
            # Calcular el color segun el estado ("agua" o "nave")
            if estado == "agua":
                color = COLOR_AGUA
            else:
                color = COLOR_NAVE
            
            # Dibujamos la casiila
            pygame.draw.rect(pantalla, color, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))
            # Borde negro
            pygame.draw.rect(pantalla, (0,0,0), (x,y,TAMANIO_CASILLA, TAMANIO_CASILLA), 2)

    # Actualiza la pantalla
    pygame.display.flip()

# Salimos de Pygame
pygame.quit()



