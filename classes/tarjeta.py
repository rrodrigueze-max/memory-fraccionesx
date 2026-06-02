# classes/tarjeta.py
import pygame
import random
import math
from config import MARRON, DORADO, VERDE_CLARO, ROJO, ROJO_CLARO
from utils.dibujos import DibujosTorta

class Tarjeta:
    """Representa una carta individual del juego"""
    
    def __init__(self, id_fraccion, tipo, numerador, denominador, color, emoji, nombre, sabor, pos_x, pos_y, ancho, alto):
        self.id_fraccion = id_fraccion
        self.tipo = tipo  # "texto" o "torta"
        self.numerador = numerador
        self.denominador = denominador
        self.color = color
        self.emoji = emoji
        self.nombre = nombre
        self.sabor = sabor
        self.rect = pygame.Rect(pos_x, pos_y, ancho, alto)
        self.visible = False
        self.emparejada = False
        
        # Helper para dibujar tortas
        self.dibujos_torta = DibujosTorta()
    
    def dibujar(self, pantalla):
        """Dibuja la tarjeta en su estado actual"""
        if self.emparejada:
            self._dibujar_emparejada(pantalla)
        elif not self.visible:
            self._dibujar_reverso(pantalla)
        else:
            self._dibujar_contenido(pantalla)
    
    def _dibujar_emparejada(self, pantalla):
        """Dibuja tarjeta ya emparejada (con brillo)"""
        glow = pygame.Surface((self.rect.w + 15, self.rect.h + 15))
        glow.set_alpha(100)
        glow.fill(VERDE_CLARO)
        pantalla.blit(glow, (self.rect.x - 7, self.rect.y - 7))
        self._dibujar_contenido(pantalla)
        for i in range(4):
            pygame.draw.rect(pantalla, DORADO, self.rect, 3, border_radius=15)
    
    def _dibujar_reverso(self, pantalla):
        """Dibuja el reverso de la tarjeta (boca abajo)"""
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.w, self.rect.h
        
        # Fondo
        pygame.draw.rect(pantalla, (255, 180, 180), self.rect, border_radius=20)
        
        # Patrón de lunares
        for i in range(12):
            px = x + random.randint(10, w-10)
            py = y + random.randint(10, h-10)
            pygame.draw.circle(pantalla, (255, 100, 100), (px, py), 4)
        
        # Marco
        pygame.draw.rect(pantalla, MARRON, self.rect, 4, border_radius=20)
        
        # Icono de regalo
        fuente = pygame.font.Font(None, int(h * 0.5))
        texto = fuente.render("🎁", True, DORADO)
        texto_rect = texto.get_rect(center=(x + w//2, y + h//2))
        pantalla.blit(texto, texto_rect)
        
        # Cinta decorativa
        pygame.draw.line(pantalla, (200, 100, 100), (x + w//2, y), (x + w//2, y + h), 3)
        pygame.draw.line(pantalla, (200, 100, 100), (x, y + h//2), (x + w, y + h//2), 3)
    
    def _dibujar_contenido(self, pantalla):
        """Dibuja el contenido de la tarjeta (boca arriba)"""
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.w, self.rect.h
        
        # Fondo con gradiente
        for i in range(4):
            color_fondo = (255 - i*12, 252 - i*10, 230 - i*8)
            pygame.draw.rect(pantalla, color_fondo, 
                           (x + i, y + i, w - 2*i, h - 2*i), 
                           border_radius=18 - i)
        
        pygame.draw.rect(pantalla, MARRON, self.rect, 3, border_radius=18)
        
        if self.tipo == "texto":
            self._dibujar_texto(pantalla, x, y, w, h)
        else:
            self.dibujos_torta.dibujar(pantalla, self.rect, self.numerador, self.denominador, self.color, self.sabor, self.nombre)
    
    def _dibujar_texto(self, pantalla, x, y, w, h):
        """Dibuja la representación textual de la fracción"""
        fuente_frac = pygame.font.Font(None, int(h * 0.45))
        
        # Sombra
        sombra = fuente_frac.render(f"{self.numerador}/{self.denominador}", True, (180, 160, 120))
        sombra_rect = sombra.get_rect(center=(x + w//2 + 3, y + h//2 + 3))
        pantalla.blit(sombra, sombra_rect)
        
        # Texto principal
        texto = fuente_frac.render(f"{self.numerador}/{self.denominador}", True, (80, 40, 20))
        texto_rect = texto.get_rect(center=(x + w//2, y + h//2))
        pantalla.blit(texto, texto_rect)
        
        # Emoji decorativo
        fuente_emoji = pygame.font.Font(None, int(h * 0.3))
        texto_emoji = fuente_emoji.render(self.emoji, True, (80, 40, 20))
        emoji_rect = texto_emoji.get_rect(center=(x + w - 25, y + 25))
        pantalla.blit(texto_emoji, emoji_rect)