import random
import json


def obtener_mejores_puntajes(puntajes_json):
    """
    Obtiene los tres mejores puntajes ordenados de mayor a menor.
    """
    # Abrimos el archivo JSON en modo lectura
    with open(puntajes_json, 'r') as archivo:
        puntajes = json.load(archivo)  # Cargamos los datos del archivo como una lista de diccionarios

    # Crear una lista para guardar puntajes válidos
    mejores_puntajes = []

    # Revisar cada elemento de los puntajes
    for elemento in puntajes:  # Iteramos por cada entrada en la lista de puntajes
        # Verificamos que cada elemento tenga las claves "nickname" y "puntaje"
        if "nickname" in elemento and "puntaje" in elemento:
            mejores_puntajes.append(elemento)  # Agregamos el elemento válido a la lista

    # Ordenar los puntajes de mayor a menor
    mejores_puntajes.sort(key=lambda x: x["puntaje"], reverse=True)  # Ordenamos por el valor de la clave "puntaje"

    # Devolver solo los tres primeros
    return mejores_puntajes[:3]  # Retornamos los tres mejores puntajes

def guardar_puntaje(archivo, nickname, puntaje):
    """
    Guarda el puntaje del jugador en un archivo JSON.
    
    Parámetros:
    - archivo: Ruta del archivo donde se almacenarán los puntajes.
    - nickname: Nombre del jugador.
    - puntaje: Puntaje del jugador.
    """
    # Leer el archivo existente
    with open(archivo, "r") as f:
        datos = json.load(f)  # Cargamos los datos existentes como una lista de diccionarios

    # Agregar nuevo puntaje
    datos.append({"nickname": nickname, "puntaje": puntaje})  # Añadimos un nuevo diccionario con los datos del jugador

    # Guardar datos actualizados
    with open(archivo, "w") as f:  # Abrimos el archivo en modo escritura
        json.dump(datos, f, indent=4)  # Escribimos la lista actualizada en formato JSON con sangría para mayor legibilidad

def pedir_nickname():
    """
    Solicita el nickname del jugador mediante consola.
    
    Retorna:
    - str: Nickname ingresado por el jugador.
    """
    nickname = input("Por favor, ingresa tu nickname: ")
    return nickname

def obtener_puntajes(archivo):
    """
    Obtiene la lista de puntajes desde un archivo JSON.
    
    Parámetros:
    - archivo: Ruta del archivo desde donde se leerán los puntajes.
    
    Retorna:
    - list: Lista de puntajes (diccionarios con nickname y puntaje).
    """
    # Abrimos el archivo JSON en modo lectura
    with open(archivo, "r") as f:
        puntajes = json.load(f)  # Cargamos los datos del archivo como una lista de diccionarios
    
    # Retornamos los puntajes cargados
    return puntajes

def obtener_datos_tablero(tablero: list):
    """ 
    Convierte el tablero en una lista de diccionarios que describe las casillas del tablero con su fila, columna y estado
    
    Parametros:
    - tablero: La matriz que representa el tablero
    
    Retorna: Una lista de diccionario, donde cada una tiene:
        - 'fila': Indice de la fila de la casilla
        - 'columna': Indice de la columna de la casilla
        - 'estado': Estado de la casilla ("agua" o "nave")
    """
    # Lista para almacenar los datos de las casillas
    datos = []

    # Recorremos las filas del tablero
    for fila in range(len(tablero)):
        # Recorremos las columnas de la fila actual
        for columna in range(len(tablero[fila])):
            # Creamos un diccionario para la casilla atual
            casilla = {}
            # Asignamos la fila
            casilla['fila'] = fila
            # Asignamos la columna
            casilla['columna'] = columna
            
            # Determinamos el estado de la casilla
            if tablero[fila][columna] == 0: # Si el valor es 0, esta vacia (agua)
                casilla['estado'] = "agua"
            # Cualquier otro valor indica la presencia de una nave
            else:
                casilla['estado'] = "nave"
            
            # Añadimos la casilla procesada a la lista de datos
            datos.append(casilla)
    
    # Retornamos la lista con los datos procesados
    
    return datos

# Crear un tablero vacio
def crear_tablero_vacio(tamano:int = 10):
    """ 
    Crea y retorna un tablero vacio representado como una matriz de 0
    
    Parametros: 
    - tamano: Tamaño del tablero (por defecto, 10x10)

    Retorna: Una lista de listas que representa el tablero vacio
    """
    
    # Inicializamos una lista vacia para representar el tablero
    tablero = []
    
    # Iteramos para cada fila
    for _ in range(tamano):
        # Creamos una nueva fila vacia
        fila = []
        # Iteramos para cada columna de la fila
        
        for _ in range(tamano):
            # Añadimos un 0, indicando que la casilla está vacia
            fila.append(0)
        
        # Añadimos la fila completa al tablero
        tablero.append(fila)
    
    # Retornamos el tablero completo
    return tablero

# Verificar si se puede colocar una nave
def puede_colocar_nave(tablero: list, fila: int, columna: int, longitud: int, orientacion: str):
    """
    Verifica si es posible colocar una nave en una posición específica del tablero.
    
    Parámetros:
    - tablero: La matriz que representa el tablero.
    - fila: Fila inicial para colocar la nave.
    - columna: Columna inicial para colocar la nave.
    - longitud: Longitud de la nave.
    - orientacion: Orientación de la nave ("horizontal" o "vertical").

    Retorna:
    - bool: True si se puede colocar la nave, False en caso contrario.
    """
    
    # Inicializamos la variable de estado
    se_puede_colocar = True

    # Verificamos cada casilla necesaria para colocar la nave
    for desplazamiento in range(longitud):
        if orientacion == "horizontal":
            # Verificamos límites y si la casilla ya está ocupada
            if columna + desplazamiento >= len(tablero[0]) or tablero[fila][columna + desplazamiento] == 1:
                se_puede_colocar = False
                break
        elif orientacion == "vertical":
            # Verificamos límites y si la casilla ya está ocupada
            if fila + desplazamiento >= len(tablero) or tablero[fila + desplazamiento][columna] == 1:
                se_puede_colocar = False
                break

    # Retornamos el estado final
    return se_puede_colocar

# Colocar una nave en el tablero
def colocar_nave(tablero: list, fila: int, columna: int, longitud: int, orientacion: str):
    """ 
    Coloca una nave en una posicion especifica del tablero
    
    Parametros:
    - tablero: La matriz que representa el tablero
    - fila: Fila inicial para colocar la nave
    - columna: Columna inicial para colocar la nave
    - longitud: Longitud de la nave
    - orientacion: Orientacion que puede ser horizontal o vertical
    
    """
    
    # Iteramos para colocar cada parte de la nave
    for desplazamiento in range(longitud):
        # Si la orientacion es horizontal
        if orientacion == "horizontal":
            # Marcamos la casilla como ocupada
            tablero[fila][columna + desplazamiento] = 1
        
        # Si la orientacion es vertical
        elif orientacion == "vertical":
            # Marcamos la casilla como ocupada
            tablero[fila + desplazamiento][columna] = 1

def generar_tablero_con_naves(tamano: int = 10):
    """
    Genera un tablero con naves colocadas aleatoriamente.
    
    Parámetros:
    - tamano: Tamaño del tablero (por defecto, 10x10).

    Retorna:
    - list: Una lista de listas que representa el tablero con las naves colocadas.
    """
    # Creamos un tablero vacío
    tablero = crear_tablero_vacio(tamano)
    
    # Lista de longitudes de las naves a colocar (2 de cada tipo)
    naves = [4, 4, 3, 3, 2, 2, 1, 1]
    
    # Iteramos sobre cada nave para colocarla en el tablero
    for nave in naves:
        # Indicamos que aún no hemos colocado la nave
        nave_colocada = False
        
        # Intentamos colocar la nave hasta que se pueda
        while not nave_colocada:
            # Generamos una fila aleatoria
            fila = random.randint(0, tamano - 1)
            # Generamos una columna aleatoria
            columna = random.randint(0, tamano - 1)
            
            # Decidimos la orientación
            if random.randint(0, 1) == 0:
                orientacion = "horizontal"
            else:
                orientacion = "vertical"
            
            # Verificamos si podemos colocar la nave
            if puede_colocar_nave(tablero, fila, columna, nave, orientacion):
                # Colocamos la nave
                colocar_nave(tablero, fila, columna, nave, orientacion)
                # Marcamos que la nave fue colocada 
                nave_colocada = True
    
    # Retornamos el tablero generado
    return tablero

def verificar_hundimiento(tablero, fila, columna):
    """
    Verifica si la nave fue hundida completamente al disparar en la posición dada.
    
    Parámetros:
    - tablero: La matriz que representa el tablero.
    - fila: Fila del disparo actual.
    - columna: Columna del disparo actual.
    
    Retorna:
    - int: Número de partes de la nave hundida o 0 si no se hundió.
    """
    partes_hundidas = 0
    # Verificar horizontalmente
    for c in range(len(tablero[0])):
        if tablero[fila][c] == 1:  # Parte de la nave
            partes_hundidas += 1
    
    # Verificar verticalmente
    for f in range(len(tablero)):
        if tablero[f][columna] == 1:  # Parte de la nave
            partes_hundidas += 1

    return partes_hundidas


