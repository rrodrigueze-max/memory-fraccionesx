# classes/efectos.py
import pygame
import random
import math
from config import DORADO

class Particula:
    """Partícula individual para efectos visuales"""
    
    def __init__(self, pos, color, velocidad=None, vida=25):
        self.pos = list(pos)
        self.vel = velocidad or [random.uniform(-4, 4), random.uniform(-7, -2)]
        self.vida = vida
        self.color = color
    
    def actualizar(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[1] += 0.2
        self.vida -= 1
        return self.vida > 0
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.pos[0]), int(self.pos[1])), 4)


class Estrella:
    """Estrella decorativa para celebraciones"""
    
    def __init__(self, pos):
        self.pos = list(pos)
        self.vel = [random.uniform(-3, 3), random.uniform(-5, -1)]
        self.vida = 20
        self.tamaño = random.randint(4, 8)
    
    def actualizar(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vida -= 1
        return self.vida > 0
    
    def dibujar(self, pantalla):
        puntos = []
        for i in range(10):
            angulo = math.radians(i * 36 - 90)
            radio = self.tamaño if i % 2 == 0 else self.tamaño // 2
            px = self.pos[0] + radio * math.cos(angulo)
            py = self.pos[1] + radio * math.sin(angulo)
            puntos.append((px, py))
        pygame.draw.polygon(pantalla, DORADO, puntos)


class Confeti:
    """Confeti para la victoria final"""
    
    def __init__(self, pantalla_ancho):
        self.x = random.randint(0, pantalla_ancho)
        self.y = random.randint(-200, -50)
        self.vel_y = random.randint(3, 8)
        self.vel_x = random.uniform(-2, 2)
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (135, 206, 235), (255, 255, 0), (255, 192, 203), (255, 140, 0)])
        self.size = random.randint(3, 8)
    
    def actualizar(self):
        self.y += self.vel_y
        self.x += self.vel_x
        return self.y < 700  # Retorna False si sale de la pantalla
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.size, self.size))