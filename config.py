# config.py
import pygame

# ==================== DIMENSIONES ====================
PANTALLA_ANCHO = 1000
PANTALLA_ALTO = 700

# ==================== COLORES ====================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (70, 130, 200)
AZUL_CLARO = (135, 206, 235)
VERDE = (50, 200, 80)
VERDE_CLARO = (100, 255, 100)
ROJO = (220, 50, 50)
ROJO_CLARO = (255, 100, 100)
AMARILLO = (255, 220, 100)
NARANJA = (255, 140, 50)
MORADO = (160, 100, 200)
GRIS = (180, 180, 180)
MARRON = (139, 69, 19)
CREMA = (255, 248, 205)
DORADO = (255, 215, 0)
ROSA = (255, 192, 203)
MENTA = (152, 255, 152)
MELON = (255, 165, 79)
CELESTE = (135, 206, 250)
LILA = (200, 150, 255)
CHOCOLATE = (101, 67, 33)
FRESA = (255, 80, 80)      # ← ESTA FALTABA
VAINILLA = (255, 248, 220)

# ==================== CONFIGURACIÓN DE NIVELES ====================
NIVELES_CONFIG = {
    1: {"nombre": "PRINCIPIANTE", "filas": 2, "columnas": 2, "pares": 2, "color": VERDE, "tiempo": 50},
    2: {"nombre": "EXPLORADOR", "filas": 3, "columnas": 3, "pares": 4, "color": AMARILLO, "tiempo": 70},
    3: {"nombre": "MAESTRO", "filas": 4, "columnas": 4, "pares": 8, "color": ROJO, "tiempo": 90},
}

# ==================== CONFIGURACIÓN DEL JUEGO ====================
FPS = 60
TIEMPO_ESPERA_ERROR = 800  # milisegundos
PUNTOS_POR_PAREJA = 10