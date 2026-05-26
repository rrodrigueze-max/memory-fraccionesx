# utils/dibujos.py
import pygame
import random
import math
import sys
import os

# Añadir el directorio padre al path para poder importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (MARRON, CHOCOLATE, ROJO, ROJO_CLARO, DORADO, BLANCO, 
                    NEGRO, NARANJA, AMARILLO, VERDE_CLARO, CELESTE, 
                    MORADO, ROSA, MENTA, MELON)

class DibujosTorta:
    """Clase especializada en dibujar tortas creativas"""
    
    def __init__(self):
        self.colores_porciones = [
            ((255, 80, 80), "🍓"),   # Rojo
            ((255, 140, 50), "🍊"),   # Naranja
            ((255, 220, 80), "🍋"),   # Amarillo
            ((100, 255, 100), "🍏"),  # Verde
            ((80, 180, 255), "🫐"),   # Azul
            ((200, 80, 255), "🍇"),   # Morado
            ((255, 100, 180), "🌸"),  # Rosa
            ((152, 255, 152), "🍈"),  # Menta
            ((255, 165, 79), "🍑")    # Melón
        ]
        
        self.frutas = {
            "fresa": ("🍓", (255, 80, 80)),
            "manzana": ("🍎", (220, 50, 50)),
            "arandano": ("🫐", (80, 180, 255)),
            "limon": ("🍋", (255, 220, 80)),
            "naranja": ("🍊", (255, 140, 50)),
            "durazno": ("🍑", (255, 165, 79)),
            "melon": ("🍈", (152, 255, 152)),
            "cereza": ("🍒", (255, 80, 80)),
            "sandia": ("🍉", (80, 200, 80)),
            "uva": ("🍇", (200, 80, 255)),
            "kiwi": ("🥝", (100, 200, 100)),
            "banana": ("🍌", (255, 220, 80)),
            "pera": ("🍐", (150, 200, 100)),
            "galleta": ("🍪", (139, 69, 19))
        }
    
    def dibujar(self, pantalla, rect, numerador, denominador, sabor, nombre):
        """Dibuja una torta creativa completa"""
        x, y, w, h = rect.x, rect.y, rect.w, rect.h
        centro_x = x + w // 2
        centro_y = y + h // 2
        radio = min(w, h) * 0.4
        radio_int = int(radio)
        
        if radio_int < 5:
            return
        
        # Sombra
        pygame.draw.circle(pantalla, (80, 60, 40), (centro_x + 5, centro_y + 5), radio_int)
        
        # Base (plato)
        self._dibujar_plato(pantalla, centro_x, centro_y, radio_int)
        
        # Cuerpo de la torta
        self._dibujar_cuerpo_torta(pantalla, centro_x, centro_y, radio_int)
        
        # Porciones
        self._dibujar_porciones(pantalla, centro_x, centro_y, radio_int, numerador, denominador)
        
        # Líneas divisoras
        self._dibujar_divisores(pantalla, centro_x, centro_y, radio_int, denominador)
        
        # Decoraciones de crema
        self._dibujar_decoraciones_crema(pantalla, centro_x, centro_y, radio_int, numerador, denominador)
        
        # Frutas decorativas
        self._dibujar_frutas(pantalla, centro_x, centro_y, radio_int, numerador, denominador, sabor)
        
        # Cereza central
        self._dibujar_cereza(pantalla, centro_x, centro_y, radio_int)
        
        # Chispitas
        self._dibujar_sprinkles(pantalla, centro_x, centro_y, radio_int)
        
        # Vela (si aplica)
        if numerador > denominador // 2:
            self._dibujar_vela(pantalla, centro_x, centro_y, radio_int)
        
        # Nombre de la torta
        self._dibujar_nombre(pantalla, x, y, w, h, nombre)
    
    def _dibujar_plato(self, pantalla, cx, cy, radio):
        plato_rect = pygame.Rect(cx - radio - 8, cy + radio - 5, radio * 2 + 16, 10)
        pygame.draw.ellipse(pantalla, (200, 200, 220), plato_rect)
        pygame.draw.ellipse(pantalla, (150, 150, 170), plato_rect, 2)
    
    def _dibujar_cuerpo_torta(self, pantalla, cx, cy, radio):
        # Capa inferior (base de chocolate)
        base_rect = pygame.Rect(cx - radio, cy + radio * 0.2, radio * 2, radio * 0.6)
        pygame.draw.rect(pantalla, (101, 67, 33), base_rect, border_radius=int(radio * 0.3))
        
        # Círculo principal
        pygame.draw.circle(pantalla, (255, 220, 150), (cx, cy), radio)
        pygame.draw.circle(pantalla, MARRON, (cx, cy), radio, 3)
    
    def _dibujar_porciones(self, pantalla, cx, cy, radio, numerador, denominador):
        if denominador == 0:
            return
        angulo_parte = 360 / denominador
        
        for i in range(numerador):
            angulo_inicio = math.radians(i * angulo_parte - 90)
            angulo_fin = math.radians((i + 1) * angulo_parte - 90)
            
            color_porcion, _ = self.colores_porciones[i % len(self.colores_porciones)]
            puntos = [(cx, cy)]
            
            num_puntos = max(12, int(angulo_parte / 3))
            for j in range(num_puntos + 1):
                t = j / num_puntos
                angulo = angulo_inicio + t * (angulo_fin - angulo_inicio)
                px = cx + radio * math.cos(angulo)
                py = cy + radio * math.sin(angulo)
                puntos.append((px, py))
            
            if len(puntos) >= 3:
                pygame.draw.polygon(pantalla, color_porcion, puntos)
                pygame.draw.polygon(pantalla, (255, 255, 200), puntos, 2)
    
    def _dibujar_divisores(self, pantalla, cx, cy, radio, denominador):
        if denominador == 0:
            return
        angulo_parte = 360 / denominador
        for i in range(denominador):
            angulo = math.radians(i * angulo_parte - 90)
            px = cx + radio * math.cos(angulo)
            py = cy + radio * math.sin(angulo)
            pygame.draw.line(pantalla, MARRON, (cx, cy), (px, py), 3)
    
    def _dibujar_decoraciones_crema(self, pantalla, cx, cy, radio, numerador, denominador):
        if denominador == 0:
            return
        angulo_parte = 360 / denominador
        
        # Rosetas de crema
        for i in range(min(numerador, len(self.colores_porciones))):
            angulo_medio = math.radians((i + 0.5) * angulo_parte - 90)
            dist_crema = radio * 0.65
            cx_crema = cx + dist_crema * math.cos(angulo_medio)
            cy_crema = cy + dist_crema * math.sin(angulo_medio)
            
            pygame.draw.circle(pantalla, (255, 250, 210), (int(cx_crema), int(cy_crema)), 6)
            pygame.draw.circle(pantalla, (255, 240, 190), (int(cx_crema), int(cy_crema)), 4)
        
        # Bordes de crema
        for ang in range(0, 360, 15):
            ang_rad = math.radians(ang)
            px = cx + (radio - 3) * math.cos(ang_rad)
            py = cy + (radio - 3) * math.sin(ang_rad)
            pygame.draw.circle(pantalla, (255, 250, 220), (int(px), int(py)), 4)
    
    def _dibujar_frutas(self, pantalla, cx, cy, radio, numerador, denominador, sabor):
        if denominador == 0:
            return
        angulo_parte = 360 / denominador
        emoji_fruta, color_fruta = self.frutas.get(sabor, ("🍰", (255, 100, 100)))
        
        for i in range(min(numerador, 3)):
            angulo_fruta = math.radians((i + 0.5) * angulo_parte - 90)
            dist_fruta = radio * 0.5
            fx = cx + dist_fruta * math.cos(angulo_fruta)
            fy = cy + dist_fruta * math.sin(angulo_fruta)
            
            pygame.draw.circle(pantalla, color_fruta, (int(fx), int(fy)), 7)
            fuente_fruta = pygame.font.Font(None, max(8, int(radio * 0.5)))
            texto_fruta = fuente_fruta.render(emoji_fruta, True, BLANCO)
            fruta_rect = texto_fruta.get_rect(center=(int(fx), int(fy)))
            pantalla.blit(texto_fruta, fruta_rect)
    
    def _dibujar_cereza(self, pantalla, cx, cy, radio):
        pygame.draw.circle(pantalla, ROJO, (cx, cy), 8)
        pygame.draw.circle(pantalla, ROJO_CLARO, (cx - 2, cy - 2), 4)
        pygame.draw.line(pantalla, (80, 60, 30), (cx, cy - 8), (cx + 5, cy - 18), 3)
    
    def _dibujar_sprinkles(self, pantalla, cx, cy, radio):
        colores_sprinkles = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 150, 255), (255, 0, 255), (255, 150, 0)]
        for _ in range(15):
            angulo = random.uniform(0, 360)
            r = radio * random.uniform(0.3, 0.85)
            sx = cx + r * math.cos(math.radians(angulo))
            sy = cy + r * math.sin(math.radians(angulo))
            color = random.choice(colores_sprinkles)
            pygame.draw.line(pantalla, color, (sx - 3, sy), (sx + 3, sy), 3)
    
    def _dibujar_vela(self, pantalla, cx, cy, radio):
        vela_x = cx
        vela_y = cy - radio - 5
        pygame.draw.rect(pantalla, (255, 200, 100), (vela_x - 3, vela_y - 15, 6, 20), border_radius=2)
        pygame.draw.circle(pantalla, (255, 215, 0), (vela_x, vela_y - 17), 5)
        pygame.draw.circle(pantalla, (255, 100, 50), (vela_x, vela_y - 18), 3)
    
    def _dibujar_nombre(self, pantalla, x, y, w, h, nombre):
        fuente_nombre = pygame.font.Font(None, max(10, int(h * 0.12)))
        texto_nombre = fuente_nombre.render(nombre, True, (80, 40, 20))
        nombre_rect = texto_nombre.get_rect(center=(x + w//2, y + h - 12))
        
        fondo_texto = pygame.Rect(nombre_rect.x - 5, nombre_rect.y - 2, nombre_rect.w + 10, nombre_rect.h + 4)
        pygame.draw.rect(pantalla, (255, 250, 220), fondo_texto, border_radius=8)
        pygame.draw.rect(pantalla, MARRON, fondo_texto, 1, border_radius=8)
        pantalla.blit(texto_nombre, nombre_rect)