# pantalla_final.py
import pygame
import random
import math
from config import *

class PantallaFinal:
    def __init__(self, pantalla, puntuacion):
        self.pantalla = pantalla
        self.puntuacion = puntuacion
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_normal = pygame.font.Font(None, 32)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        self.dialogos = [
            "🎉 ¡LO LOGRASTE, GRAN CHEF! 🎉",
            "🍰 Gracias a ti, Don Repostero recuperó",
            "📖 todas las recetas perdidas...",
            "👾 ¡El Monstruo de las Fracciones huyó!",
            "🏆 Ahora eres un CHEF HONORARIO",
            "⭐ de la pastelería mágica.",
            "",
            "🍕 ¡Vuelve cuando quieras a practicar!",
            "🎮 ¡Siempre tendrás un lugar aquí!",
            "",
            "👉 PRESIONA ESPACIO 👈"
        ]
        
        self.dialogo_actual = 0
        self.tiempo_ultimo_dialogo = 0
        self.animacion_frame = 0
        self.confeti = []
        self.estrellas = []
        self._crear_confeti()
        self._crear_estrellas()
        self.fondo = None
        self._crear_fondo()
    
    def _crear_fondo(self):
        self.fondo = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        colores = [(255, 100, 100), (255, 180, 80), (255, 240, 80), (100, 200, 100), (80, 180, 255), (200, 100, 255)]
        ancho_banda = PANTALLA_ANCHO // len(colores)
        for i, color in enumerate(colores):
            pygame.draw.rect(self.fondo, color, (i * ancho_banda, 0, ancho_banda, PANTALLA_ALTO))
    
    def _crear_confeti(self):
        for _ in range(100):
            self.confeti.append({
                'x': random.randint(0, PANTALLA_ANCHO),
                'y': random.randint(-500, -50),
                'vel_y': random.randint(3, 8),
                'vel_x': random.uniform(-2, 2),
                'color': random.choice([ROJO, AMARILLO, VERDE, AZUL_CLARO, ROSA, NARANJA]),
                'tamano': random.randint(4, 8)
            })
    
    def _crear_estrellas(self):
        for _ in range(50):
            self.estrellas.append({
                'x': random.randint(0, PANTALLA_ANCHO),
                'y': random.randint(0, PANTALLA_ALTO),
                'brillo': random.randint(50, 255),
                'direccion': 5
            })
    
    def _actualizar_confeti(self):
        for conf in self.confeti:
            conf['y'] += conf['vel_y']
            conf['x'] += conf['vel_x']
            if conf['y'] > PANTALLA_ALTO:
                conf['y'] = -20
                conf['x'] = random.randint(0, PANTALLA_ANCHO)
    
    def _actualizar_estrellas(self):
        for estrella in self.estrellas:
            estrella['brillo'] += estrella['direccion']
            if estrella['brillo'] >= 255:
                estrella['brillo'] = 255
                estrella['direccion'] = -5
            elif estrella['brillo'] <= 50:
                estrella['brillo'] = 50
                estrella['direccion'] = 5
    
    def _dibujar_chef_nino_feliz(self, x, y):
        self.animacion_frame += 0.1
        salto = int(math.sin(self.animacion_frame) * 5)
        
        pygame.draw.circle(self.pantalla, (255, 220, 150), (x, y + salto), 55)
        pygame.draw.arc(self.pantalla, NEGRO, (x - 32, y - 10 + salto, 25, 15), 0, math.pi, 4)
        pygame.draw.arc(self.pantalla, NEGRO, (x + 7, y - 10 + salto, 25, 15), 0, math.pi, 4)
        pygame.draw.arc(self.pantalla, NEGRO, (x - 28, y + 5 + salto, 56, 35), 0, math.pi, 6)
        pygame.draw.circle(self.pantalla, (255, 150, 150), (x - 40, y + 5 + salto), 10)
        pygame.draw.circle(self.pantalla, (255, 150, 150), (x + 40, y + 5 + salto), 10)
        pygame.draw.rect(self.pantalla, BLANCO, (x - 35, y - 60 + salto, 70, 30), border_radius=10)
        pygame.draw.ellipse(self.pantalla, BLANCO, (x - 25, y - 85 + salto, 50, 35))
        pygame.draw.line(self.pantalla, (255, 220, 150), (x - 45, y + 10 + salto), (x - 75, y - 20 + salto), 12)
        pygame.draw.line(self.pantalla, (255, 220, 150), (x + 45, y + 10 + salto), (x + 75, y - 20 + salto), 12)
        pygame.draw.circle(self.pantalla, (255, 220, 150), (x - 77, y - 22 + salto), 8)
        pygame.draw.circle(self.pantalla, (255, 220, 150), (x + 77, y - 22 + salto), 8)
        
        pygame.draw.polygon(self.pantalla, DORADO, [
            (x - 30, y - 65 + salto), (x - 15, y - 50 + salto),
            (x, y - 70 + salto), (x + 15, y - 50 + salto),
            (x + 30, y - 65 + salto)
        ])
    
    def _dibujar_don_repostero(self, x, y):
        pygame.draw.rect(self.pantalla, (200, 200, 200), (x - 15, y - 10, 30, 45), border_radius=8)
        pygame.draw.circle(self.pantalla, (255, 220, 180), (x, y - 28), 22)
        pygame.draw.rect(self.pantalla, BLANCO, (x - 18, y - 55, 36, 30), border_radius=5)
        pygame.draw.ellipse(self.pantalla, BLANCO, (x - 12, y - 65, 24, 18))
        pygame.draw.arc(self.pantalla, NEGRO, (x - 15, y - 35, 14, 8), 0, math.pi, 2)
        pygame.draw.arc(self.pantalla, NEGRO, (x + 1, y - 35, 14, 8), 0, math.pi, 2)
        pygame.draw.line(self.pantalla, (100, 80, 50), (x - 12, y - 22), (x, y - 20), 3)
        pygame.draw.line(self.pantalla, (100, 80, 50), (x + 12, y - 22), (x, y - 20), 3)
        pygame.draw.arc(self.pantalla, NEGRO, (x - 10, y - 22, 20, 12), 0, math.pi, 2)
    
    def _dibujar_burbuja(self, texto, x, y):
        texto_render = self.fuente_normal.render(texto, True, NEGRO)
        ancho = texto_render.get_width() + 40
        alto = texto_render.get_height() + 20
        burbuja = pygame.Rect(x - ancho // 2, y - alto - 20, ancho, alto)
        pygame.draw.rect(self.pantalla, BLANCO, burbuja, border_radius=20)
        pygame.draw.rect(self.pantalla, NEGRO, burbuja, 2, border_radius=20)
        self.pantalla.blit(texto_render, (x - texto_render.get_width() // 2, y - alto - 10))
    
    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        
        self._actualizar_confeti()
        self._actualizar_estrellas()
        
        for conf in self.confeti:
            pygame.draw.rect(self.pantalla, conf['color'], (conf['x'], conf['y'], conf['tamano'], conf['tamano']))
        
        for estrella in self.estrellas:
            brillo = estrella['brillo']
            pygame.draw.circle(self.pantalla, (brillo, brillo, 100), (int(estrella['x']), int(estrella['y'])), 3)
        
        titulo = self.fuente_titulo.render("🌟 ¡MISIÓN CUMPLIDA! 🌟", True, DORADO)
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO // 2, 50))
        self.pantalla.blit(titulo, titulo_rect)
        
        self._dibujar_chef_nino_feliz(180, PANTALLA_ALTO - 200)
        self._dibujar_don_repostero(PANTALLA_ANCHO - 150, PANTALLA_ALTO - 180)
        
        if self.dialogo_actual < len(self.dialogos):
            if self.dialogos[self.dialogo_actual] != "":
                self._dibujar_burbuja(self.dialogos[self.dialogo_actual], PANTALLA_ANCHO // 2, PANTALLA_ALTO - 100)
        
        puntos_texto = self.fuente_normal.render(f"⭐ PUNTUACIÓN: {self.puntuacion} ⭐", True, (255, 215, 0))
        puntos_rect = puntos_texto.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO - 50))
        pygame.draw.rect(self.pantalla, (60, 50, 70), puntos_rect.inflate(30, 10), border_radius=15)
        self.pantalla.blit(puntos_texto, puntos_rect)
        
        if pygame.time.get_ticks() // 500 % 2 == 0:
            texto = self.fuente_pequena.render("👉 PRESIONA ESPACIO 👈", True, (255, 100, 50))
            texto_rect = texto.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO - 25))
            pygame.draw.rect(self.pantalla, (255, 255, 200), texto_rect.inflate(20, 10), border_radius=15)
            self.pantalla.blit(texto, texto_rect)
    
    def esperar_inicio(self):
        esperando = True
        reloj = pygame.time.Clock()
        self.tiempo_ultimo_dialogo = pygame.time.get_ticks()
        
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.dialogo_actual < len(self.dialogos) - 1:
                            self.dialogo_actual += 1
                            self.tiempo_ultimo_dialogo = pygame.time.get_ticks()
                        else:
                            esperando = False
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            if pygame.time.get_ticks() - self.tiempo_ultimo_dialogo > 3000:
                if self.dialogo_actual < len(self.dialogos) - 1:
                    self.dialogo_actual += 1
                    self.tiempo_ultimo_dialogo = pygame.time.get_ticks()
            
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        
        return True