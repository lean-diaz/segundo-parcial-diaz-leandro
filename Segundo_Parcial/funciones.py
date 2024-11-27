import random

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

# Generar un tablero con naves aleatorias
def generar_tablero_con_naves(tamano:int = 10):
    """
    Genera un tablero con naves colocadas aleatoriamente.
    
    Parámetros:
    - tamano: Tamaño del tablero (por defecto, 10x10).

    Retorna:
    - list: Una lista de listas que representa el tablero con las naves colocadas.
    """
    
    # Creamos un tablero vacio
    tablero = crear_tablero_vacio(tamano)
    
    # Lista de longitudes de las naves a colocar
    naves = [4,3,2,1]
    
    # Iteramos sobre cada nave para colocarla en el tablero
    for nave in naves:
        # Indicamos que aun no hemos colocado la nave
        nave_colocada = False
        
        # Intentamos colocar la nave hasta que se pueda
        while not nave_colocada:
            # Generamos una fila aleatoria
            fila = random.randint(0, tamano - 1)
            # Generamos una columna aleatoria
            columna = random.randint(0, tamano - 1)
            
            # Decidimos la orientacion
            if random.randint(0,1) == 0:
                orientacion = "horizontal"
            else:
                orientacion = "vertical"
            
            # Verificamos si podemos colocar la nave
            if puede_colocar_nave(tablero, fila, columna, nave, orientacion):
                # Colocamos la nave
                colocar_nave(tablero, fila, columna, nave, orientacion)
                # Marcamos que la nave fue colocada 
                nave_colocada = True
    
    # Retornamos el tablero  generado
    return tablero



