# utils/dibujos.py
import pygame
import math
from config import *

class DibujosTorta:
    """Dibuja tortas y pizzas CLARAS para niños - SIN número de fracción"""
    
    def dibujar(self, pantalla, rect, numerador, denominador, sabor, nombre):
        x, y, w, h = rect.x, rect.y, rect.w, rect.h
        centro_x = x + w // 2
        centro_y = y + h // 2
        radio = min(w, h) * 0.45
        r = int(radio)
        
        # Fondo de la tarjeta
        pygame.draw.rect(pantalla, (255, 248, 220), rect, border_radius=15)
        pygame.draw.rect(pantalla, MARRON, rect, 3, border_radius=15)
        
        # ========== DIBUJAR EL CÍRCULO BASE ==========
        if sabor == "pizza":
            pygame.draw.circle(pantalla, (255, 200, 100), (centro_x, centro_y), r)
            pygame.draw.circle(pantalla, (180, 100, 50), (centro_x, centro_y), r, 3)
            pygame.draw.circle(pantalla, (255, 120, 80), (centro_x, centro_y), r-5, 2)
        else:
            pygame.draw.circle(pantalla, (255, 220, 160), (centro_x, centro_y), r)
            pygame.draw.circle(pantalla, MARRON, (centro_x, centro_y), r, 3)
        
        # Colores brillantes para las porciones
        colores_porciones = [
            (255, 70, 70),   # Rojo
            (70, 200, 70),   # Verde
            (70, 120, 255),  # Azul
            (255, 200, 70),  # Amarillo
            (200, 70, 255),  # Morado
            (255, 120, 180), # Rosa
            (70, 200, 200),  # Turquesa
            (255, 160, 70),  # Naranja
        ]
        
        # ========== DIBUJAR LAS PORCIONES ==========
        if denominador > 0 and numerador > 0:
            angulo_parte = 360 / denominador
            
            for i in range(numerador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                
                puntos = [(centro_x, centro_y)]
                
                for paso in range(16):
                    t = paso / 15
                    angulo = inicio + t * (fin - inicio)
                    px = centro_x + r * math.cos(angulo)
                    py = centro_y + r * math.sin(angulo)
                    puntos.append((px, py))
                
                color = colores_porciones[i % len(colores_porciones)]
                pygame.draw.polygon(pantalla, color, puntos)
                pygame.draw.polygon(pantalla, NEGRO, puntos, 2)
            
            # Líneas divisoras
            for i in range(denominador):
                angulo = math.radians(i * angulo_parte - 90)
                px = centro_x + r * math.cos(angulo)
                py = centro_y + r * math.sin(angulo)
                pygame.draw.line(pantalla, NEGRO, (centro_x, centro_y), (px, py), 3)
        
        # ========== DECORACIÓN PARA PIZZA ==========
        if sabor == "pizza" and numerador > 0:
            angulo_parte = 360 / denominador
            for i in range(min(numerador, 6)):
                angulo = math.radians((i + 0.5) * angulo_parte - 90)
                dist = r * 0.55
                px = centro_x + dist * math.cos(angulo)
                py = centro_y + dist * math.sin(angulo)
                pygame.draw.circle(pantalla, (180, 40, 40), (int(px), int(py)), max(4, r//6))
        
        # ========== NOMBRE DE LA TORTA/PIZZA ==========
        fuente_nom = pygame.font.Font(None, max(10, int(h * 0.12)))
        texto_nom = fuente_nom.render(nombre, True, (80, 50, 25))
        nom_rect = texto_nom.get_rect(center=(x + w//2, y + h - 12))
        
        fondo_nom = pygame.Rect(nom_rect.x - 4, nom_rect.y - 2, nom_rect.w + 8, nom_rect.h + 4)
        pygame.draw.rect(pantalla, (255, 250, 220), fondo_nom, border_radius=6)
        pygame.draw.rect(pantalla, MARRON, fondo_nom, 1, border_radius=6)
        pantalla.blit(texto_nom, nom_rect)