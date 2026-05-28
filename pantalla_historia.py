# pantalla_historia.py
import os
import pygame
import random
import math
from config import *

class PantallaHistoria:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_normal = pygame.font.Font(None, 32)
        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Animación
        self.animacion_frame = 0
        self.chef_frames = []
        self.chef_frame_index = 0.0
        self.globos_flotando = []
        self._crear_globos()
        self._cargar_chef_frames()
        
        # Diálogos del personaje
        self.dialogos = [
            "¡Hola! ¡Soy Nico, tu chef amigo!",
            "¡AYUDA! El monstruo se llevó mis recetas...",
            "Las escondió en estas tarjetas mágicas.",
            "Usa tu MEMORIA para encontrar las parejas.",
            "Cada pareja correcta = ¡10 PUNTOS!",
            "Completa los 3 niveles = ¡MEDALLA DE ORO!",
            "¿Listo para la aventura? ¡VAMOS!"
        ]
        
        self.dialogo_actual = 0
        self.tiempo_ultimo_dialogo = 0
        self.mostrando_dialogo = True
        
        # Fondo
        self.fondo = None
        self._crear_fondo()
    
    def _crear_fondo(self):
        """Crea fondo colorido y alegre"""
        self.fondo = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        
        # Cielo arcoíris
        colores = [
            (255, 100, 100),  # Rojo
            (255, 180, 80),   # Naranja
            (255, 240, 80),   # Amarillo
            (100, 200, 100),  # Verde
            (80, 180, 255),   # Azul
            (200, 100, 255),  # Morado
        ]
        
        ancho_banda = PANTALLA_ANCHO // len(colores)
        for i, color in enumerate(colores):
            pygame.draw.rect(self.fondo, color, (i * ancho_banda, 0, ancho_banda, PANTALLA_ALTO))
        
        # Nubes
        for i in range(5):
            x = random.randint(0, PANTALLA_ANCHO)
            y = random.randint(20, 200)
            pygame.draw.ellipse(self.fondo, (255, 255, 255), (x, y, 100, 60))
            pygame.draw.ellipse(self.fondo, (255, 255, 255), (x + 40, y - 20, 80, 50))
    
    def _crear_globos(self):
        """Crea globos flotantes"""
        for _ in range(8):
            self.globos_flotando.append({
                'x': random.randint(50, PANTALLA_ANCHO - 50),
                'y': random.randint(100, PANTALLA_ALTO - 100),
                'vel_y': random.uniform(0.5, 1.5),
                'color': random.choice([(255, 100, 100), (255, 200, 100), (100, 200, 255)]),
                'tamano': random.randint(20, 35)
            })
    
    def _cargar_chef_frames(self):
        """Carga los frames animados del chef desde assets"""
        carpeta = os.path.join("assets", "chef_frames")
        if not os.path.isdir(carpeta):
            return
        nombres = sorted([nombre for nombre in os.listdir(carpeta) if nombre.lower().endswith(".png")])
        for nombre in nombres:
            try:
                ruta = os.path.join(carpeta, nombre)
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.smoothscale(imagen, (380, 450))
                self.chef_frames.append(imagen)
            except pygame.error:
                pass
    
    def _dibujar_personaje_principal(self, x, y):
        """Dibuja a un chef niño con estilo alegre y colorido"""

        # Animación de salto y brillo
        self.animacion_frame += 0.12
        salto = int(math.sin(self.animacion_frame) * 6)
        brillo = 200 + int(30 * math.sin(self.animacion_frame * 1.5))
        color_cara = (255, 230, 200)

        # ========== CUERPO ==========
        pygame.draw.ellipse(self.pantalla, (120, 190, 255), (x - 36, y - 10 + salto, 72, 90))
        pygame.draw.rect(self.pantalla, (255, 220, 120), (x - 32, y + 30 + salto, 64, 45), border_radius=16)
        pygame.draw.rect(self.pantalla, (255, 170, 220), (x - 24, y + 38 + salto, 48, 30), border_radius=14)

        # ========== CARA ==========
        pygame.draw.circle(self.pantalla, color_cara, (x, y - 35 + salto), 30)
        pygame.draw.circle(self.pantalla, BLANCO, (x - 14, y - 40 + salto), 12)
        pygame.draw.circle(self.pantalla, BLANCO, (x + 14, y - 40 + salto), 12)
        pygame.draw.circle(self.pantalla, NEGRO, (x - 14, y - 40 + salto), 6)
        pygame.draw.circle(self.pantalla, NEGRO, (x + 14, y - 40 + salto), 6)
        pygame.draw.circle(self.pantalla, (255, 180, 180), (x - 18, y - 28 + salto), 6)
        pygame.draw.circle(self.pantalla, (255, 180, 180), (x + 18, y - 28 + salto), 6)
        pygame.draw.arc(self.pantalla, NEGRO, (x - 16, y - 28 + salto, 32, 24), math.pi, 2 * math.pi, 4)

        # Pelo alegre asomando bajo el gorro
        pygame.draw.arc(self.pantalla, (200, 120, 70), (x - 28, y - 55 + salto, 20, 24), math.pi, 2 * math.pi, 12)
        pygame.draw.arc(self.pantalla, (200, 120, 70), (x + 8, y - 55 + salto, 20, 24), math.pi, 2 * math.pi, 12)
        pygame.draw.polygon(self.pantalla, (200, 120, 70), [(x - 15, y - 55 + salto), (x + 15, y - 55 + salto), (x, y - 70 + salto)])

        # ========== GORRO DE CHEF ==========
        pygame.draw.rect(self.pantalla, BLANCO, (x - 32, y - 70 + salto, 64, 25), border_radius=12)
        pygame.draw.ellipse(self.pantalla, BLANCO, (x - 28, y - 95 + salto, 56, 42))
        pygame.draw.ellipse(self.pantalla, (230, 230, 230), (x - 22, y - 90 + salto, 44, 28))

        # ========== BRAZOS ==========
        brazo_izq_y = y + 6 + salto + int(math.sin(self.animacion_frame * 2) * 4)
        brazo_izq_x = x - 35
        pygame.draw.line(self.pantalla, color_cara, (x - 20, y + 10 + salto), (brazo_izq_x, brazo_izq_y), 12)
        pygame.draw.circle(self.pantalla, color_cara, (brazo_izq_x, brazo_izq_y), 8)

        brazo_der_y = y + 8 + salto + int(math.cos(self.animacion_frame * 2) * 4)
        brazo_der_x = x + 35
        pygame.draw.line(self.pantalla, color_cara, (x + 20, y + 10 + salto), (brazo_der_x, brazo_der_y), 12)
        pygame.draw.circle(self.pantalla, color_cara, (brazo_der_x, brazo_der_y), 8)

        # Espátula divertida en mano
        pygame.draw.line(self.pantalla, (180, 180, 200), (brazo_der_x, brazo_der_y), (brazo_der_x + 18, brazo_der_y - 10), 6)
        pygame.draw.rect(self.pantalla, (240, 240, 240), (brazo_der_x + 15, brazo_der_y - 18, 20, 10), border_radius=4)

        # ========== PIERNAS Y ZAPATOS ==========
        pygame.draw.line(self.pantalla, (255, 220, 120), (x - 14, y + 70 + salto), (x - 18, y + 95 + salto), 10)
        pygame.draw.line(self.pantalla, (255, 220, 120), (x + 14, y + 70 + salto), (x + 18, y + 95 + salto), 10)
        pygame.draw.ellipse(self.pantalla, (120, 150, 200), (x - 28, y + 92 + salto, 22, 12))
        pygame.draw.ellipse(self.pantalla, (120, 150, 200), (x + 6, y + 92 + salto, 22, 12))

        # ========== DELANTAL Y DETALLES ==========
        pygame.draw.rect(self.pantalla, (255, 255, 255), (x - 18, y - 2 + salto, 36, 50), border_radius=12)
        pygame.draw.ellipse(self.pantalla, (255, 200, 200), (x - 16, y + 6 + salto, 32, 14))
        pygame.draw.circle(self.pantalla, (255, 180, 180), (x, y + 18 + salto), 4)

        # Detalles brillantes
        for i in range(3):
            px = x + int(math.cos(self.animacion_frame + i * 2) * 26)
            py = y - 20 + salto + int(math.sin(self.animacion_frame + i * 1.5) * 12)
            pygame.draw.circle(self.pantalla, (255, 255, 180), (px, py), 4)
            pygame.draw.circle(self.pantalla, (255, 110, 180), (px + 2, py - 2), 2)

    def _dibujar_chef_animado(self, x, y):
        """Dibuja al chef niño usando frames animados"""
        if self.chef_frames:
            self.chef_frame_index += 0.15
            if self.chef_frame_index >= len(self.chef_frames):
                self.chef_frame_index = 0.0
            frame = self.chef_frames[int(self.chef_frame_index)]
            rect = frame.get_rect(midbottom=(x, y))
            self.pantalla.blit(frame, rect)
        else:
            self._dibujar_personaje_principal(x, y)
    
    def _wrap_text(self, texto, fuente, max_width):
        palabras = texto.split(" ")
        lineas = []
        linea = ""
        for palabra in palabras:
            prueba = linea + (" " if linea else "") + palabra
            if fuente.size(prueba)[0] <= max_width:
                linea = prueba
            else:
                if linea:
                    lineas.append(linea)
                linea = palabra
        if linea:
            lineas.append(linea)
        return lineas

    def _dibujar_burbuja_dialogo(self, texto, x, y):
        """Dibuja burbuja de diálogo"""
        lineas = self._wrap_text(texto, self.fuente_dialogo, 340)
        ancho = max(self.fuente_dialogo.size(linea)[0] for linea in lineas) + 40
        alto = len(lineas) * self.fuente_dialogo.get_height() + 30
        burbuja_rect = pygame.Rect(x - ancho // 2, y - alto - 20, ancho, alto)
        pygame.draw.rect(self.pantalla, BLANCO, burbuja_rect, border_radius=24)
        pygame.draw.rect(self.pantalla, NEGRO, burbuja_rect, 3, border_radius=24)
        pygame.draw.polygon(self.pantalla, BLANCO, [(x, y - 15), (x - 18, y - 35), (x + 18, y - 35)])
        pygame.draw.polygon(self.pantalla, NEGRO, [(x, y - 15), (x - 18, y - 35), (x + 18, y - 35)], 2)
        for i, linea in enumerate(lineas):
            texto_render = self.fuente_dialogo.render(linea, True, NEGRO)
            tx = x - texto_render.get_width() // 2
            ty = y - alto - 10 + i * self.fuente_dialogo.get_height()
            self.pantalla.blit(texto_render, (tx, ty))
    
    def _dibujar_monstruo(self, x, y):
        """Dibuja monstruo divertido (no da miedo)"""
        # Cuerpo
        pygame.draw.ellipse(self.pantalla, (150, 255, 150), (x - 30, y - 25, 60, 50))
        # Ojos grandes
        pygame.draw.circle(self.pantalla, BLANCO, (x - 12, y - 15), 10)
        pygame.draw.circle(self.pantalla, BLANCO, (x + 12, y - 15), 10)
        pygame.draw.circle(self.pantalla, NEGRO, (x - 12, y - 15), 5)
        pygame.draw.circle(self.pantalla, NEGRO, (x + 12, y - 15), 5)
        # Boca asustada
        pygame.draw.ellipse(self.pantalla, NEGRO, (x - 12, y + 2, 24, 12))
        # Cuernitos
        pygame.draw.line(self.pantalla, (150, 255, 150), (x - 15, y - 45), (x - 25, y - 60), 5)
        pygame.draw.line(self.pantalla, (150, 255, 150), (x + 15, y - 45), (x + 25, y - 60), 5)
        
        # Cartel "¡Qué miedo!"
        texto = self.fuente_pequena.render(" ¡Huy!", True, (0, 0, 0))
        self.pantalla.blit(texto, (x - 35, y - 75))
    
    def _dibujar_chef_gif(self, x, y):
        """Dibuja un efecto animado tipo GIF alrededor del chef niño"""
        fase = (pygame.time.get_ticks() / 200) % 4
        brillo = 180 + int(40 * math.sin(pygame.time.get_ticks() / 250))
        color_base = (brillo, 230, 255)
        for i in range(5):
            ang = self.animacion_frame + i * 1.25
            radio = 75 + 6 * math.sin(ang)
            alpha = 120 + int(80 * math.cos(ang * 0.7))
            x_offset = x + int(math.cos(ang) * radio * 0.2)
            y_offset = y - 30 + int(math.sin(ang) * radio * 0.1)
            circulo = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(circulo, (*color_base, max(20, min(140, alpha))), (60, 60), int(28 + 4 * math.sin(ang * 1.5)))
            self.pantalla.blit(circulo, (x_offset - 60, y_offset - 60))
        # Estrellas alrededor del chef
        for i in range(6):
            ang = self.animacion_frame + i * 1.05
            r = 95 + 8 * math.cos(self.animacion_frame * 1.2 + i)
            sx = x + int(math.cos(ang) * r)
            sy = y - 40 + int(math.sin(ang) * (r * 0.3))
            radio = 3 + int(2 * abs(math.sin(self.animacion_frame + i)))
            pygame.draw.circle(self.pantalla, (255, 255, 180), (sx, sy), radio)
            pygame.draw.circle(self.pantalla, (255, 180, 220), (sx + 2, sy - 2), max(1, radio - 1))
    
    def _dibujar_estrellas(self):
        """Dibuja estrellas brillantes"""
        tiempo = pygame.time.get_ticks() / 500
        for i in range(15):
            x = (i * 100 + tiempo * 50) % PANTALLA_ANCHO
            y = 50 + math.sin(i) * 20
            pygame.draw.circle(self.pantalla, DORADO, (int(x), int(y)), 4)
            pygame.draw.circle(self.pantalla, (255, 255, 150), (int(x), int(y)), 2)
    
    def dibujar(self):
        """Dibuja toda la pantalla"""
        self.pantalla.blit(self.fondo, (0, 0))
        
        # Dibujar globos
        for globo in self.globos_flotando:
            globo['y'] -= globo['vel_y']
            if globo['y'] < -50:
                globo['y'] = PANTALLA_ALTO + 50
                globo['x'] = random.randint(50, PANTALLA_ANCHO - 50)
            pygame.draw.circle(self.pantalla, globo['color'], (int(globo['x']), int(globo['y'])), globo['tamano'])
            pygame.draw.line(self.pantalla, (100, 100, 100), (int(globo['x']), int(globo['y']) + globo['tamano']), (int(globo['x']), int(globo['y']) + globo['tamano'] + 20), 2)
        
        # Estrellas
        self._dibujar_estrellas()
        
        # Título
        titulo = self.fuente_titulo.render("¡AVENTURA EN LA PASTELERÍA!", True, DORADO)
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO // 2, 40))
        sombra = self.fuente_titulo.render("¡AVENTURA EN LA PASTELERÍA!", True, (100, 80, 20))
        sombra_rect = sombra.get_rect(center=(PANTALLA_ANCHO // 2 + 3, 43))
        self.pantalla.blit(sombra, sombra_rect)
        self.pantalla.blit(titulo, titulo_rect)
        
        # Personaje principal con animación de frames
        self._dibujar_chef_animado(260, PANTALLA_ALTO - 90)
        
        # Monstruo (escondido)
        self._dibujar_monstruo(PANTALLA_ANCHO - 120, PANTALLA_ALTO - 180)
        
        # Burbuja de diálogo
        if self.mostrando_dialogo and self.dialogo_actual < len(self.dialogos):
            self._dibujar_burbuja_dialogo(self.dialogos[self.dialogo_actual], 500, PANTALLA_ALTO - 230)
        
        # Instrucción
        if pygame.time.get_ticks() // 500 % 2 == 0:
            instruccion = self.fuente_normal.render(" PRESIONA ESPACIO ", True, (255, 100, 50))
            instruccion_rect = instruccion.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO - 60))
            
            # Fondo
            fondo_rect = pygame.Rect(instruccion_rect.x - 15, instruccion_rect.y - 8, instruccion_rect.w + 30, instruccion_rect.h + 16)
            pygame.draw.rect(self.pantalla, (255, 255, 200), fondo_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, MARRON, fondo_rect, 3, border_radius=20)
            self.pantalla.blit(instruccion, instruccion_rect)
    
    def esperar_inicio(self):
        """Espera ESPACIO con animación de diálogos"""
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
                            # Siguiente diálogo
                            self.dialogo_actual += 1
                            self.tiempo_ultimo_dialogo = pygame.time.get_ticks()
                        else:
                            esperando = False
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            # Cambiar diálogo automáticamente cada 3 segundos
            if pygame.time.get_ticks() - self.tiempo_ultimo_dialogo > 3000:
                if self.dialogo_actual < len(self.dialogos) - 1:
                    self.dialogo_actual += 1
                    self.tiempo_ultimo_dialogo = pygame.time.get_ticks()
            
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        
        return True