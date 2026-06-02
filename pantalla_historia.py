# pantalla_historia.py
import os
import pygame
import random
import math
from config import *
from PIL import Image

class PantallaHistoria:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_normal = pygame.font.Font(None, 32)
        self.fuente_dialogo = pygame.font.Font(None, 24)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Animación
        self.animacion_frame = 0
        self.chef_frames = []
        self.chef_frame_index = 0.0
        self.globos_flotando = []
        self._crear_globos()
        self._cargar_chef_frames()

        # Imagen de entrada personalizada
        self.custom_entrance_image = None
        custom_path = "/home/ramiro/Descargas/foto1.png"
        try:
            if os.path.isfile(custom_path):
                img = pygame.image.load(custom_path).convert_alpha()
                self.custom_entrance_image = pygame.transform.smoothscale(img, (PANTALLA_ANCHO, PANTALLA_ALTO))
                print("✅ Imagen de fondo personalizada cargada")
        except Exception:
            self.custom_entrance_image = None
        
        # Cargar GIF de pizza animado
        self.pizza_frames = []
        self.pizza_frame_index = 0
        self.pizza_ultimo_cambio = 0
        self.pizza_frame_delay = 100
        self.pizza_gif_rect = None
        self._cargar_pizza_gif()
        
        # Diálogos
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
        
        # Fondo alternativo
        self.fondo = None
        self._crear_fondo()
    
    def _crear_fondo(self):
        """Crea fondo colorido y alegre"""
        self.fondo = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        
        colores = [
            (255, 100, 100), (255, 180, 80), (255, 240, 80),
            (100, 200, 100), (80, 180, 255), (200, 100, 255),
        ]
        
        ancho_banda = PANTALLA_ANCHO // len(colores)
        for i, color in enumerate(colores):
            pygame.draw.rect(self.fondo, color, (i * ancho_banda, 0, ancho_banda, PANTALLA_ALTO))
        
        for i in range(5):
            x = random.randint(0, PANTALLA_ANCHO)
            y = random.randint(20, 200)
            pygame.draw.ellipse(self.fondo, (255, 255, 255), (x, y, 100, 60))
            pygame.draw.ellipse(self.fondo, (255, 255, 255), (x + 40, y - 20, 80, 50))
    
    def _crear_globos(self):
        for _ in range(8):
            self.globos_flotando.append({
                'x': random.randint(50, PANTALLA_ANCHO - 50),
                'y': random.randint(100, PANTALLA_ALTO - 100),
                'vel_y': random.uniform(0.5, 1.5),
                'color': random.choice([(255, 100, 100), (255, 200, 100), (100, 200, 255)]),
                'tamano': random.randint(20, 35)
            })
    
    def _cargar_chef_frames(self):
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
    
    def _cargar_pizza_gif(self):
        gif_path = "/home/ramiro/Descargas/112.gif"
        
        if not os.path.isfile(gif_path):
            print(f"❌ No se encontró: {gif_path}")
            self.pizza_frames = []
            return
        
        try:
            print(f"✅ Cargando GIF: {gif_path}")
            pil_gif = Image.open(gif_path)
            frames = []
            print(f"📀 GIF tiene {pil_gif.n_frames} frames")
            
            for frame_num in range(pil_gif.n_frames):
                pil_gif.seek(frame_num)
                if pil_gif.mode != 'RGB':
                    frame_rgb = pil_gif.convert('RGB')
                else:
                    frame_rgb = pil_gif.copy()
                
                frame_surface = pygame.image.fromstring(
                    frame_rgb.tobytes(), 
                    frame_rgb.size, 
                    'RGB'
                ).convert_alpha()
                
                frame_surface = pygame.transform.smoothscale(frame_surface, (60, 70))
                frames.append(frame_surface)
            
            self.pizza_frames = frames
            self.pizza_frame_index = 0
            self.pizza_ultimo_cambio = pygame.time.get_ticks()
            self.pizza_gif_rect = frames[0].get_rect(topleft=(444, 200))
            print(f"✅ Pizza GIF cargada: {len(frames)} frames")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.pizza_frames = []
    
    def _actualizar_animacion_pizza(self):
        if not self.pizza_frames or len(self.pizza_frames) <= 1:
            return
        ahora = pygame.time.get_ticks()
        if ahora - self.pizza_ultimo_cambio >= self.pizza_frame_delay:
            self.pizza_frame_index = (self.pizza_frame_index + 1) % len(self.pizza_frames)
            self.pizza_ultimo_cambio = ahora
    
    def _dibujar_personaje_principal(self, x, y):
        """Dibuja al chef (NO SE USA ACTUALMENTE)"""
        pass  # Vacío porque no queremos mostrar el muñeco
    
    def _dibujar_chef_animado(self, x, y):
        """No dibuja nada - muñeco eliminado"""
        pass  # No dibujar el chef
    
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
    
    def _dibujar_cuadro_instrucciones(self):
        ancho = 300
        x = PANTALLA_ANCHO - ancho - 20
        y = 90

        instrucciones = [
            "Busca las cartas que tienen la misma fracción.",
            "Haz clic en dos cartas para voltearlas.",
            "Encuentra todas antes de que se acabe el tiempo.",
        ]

        max_texto_ancho = ancho - 30
        lineas = []
        for instruccion in instrucciones:
            lineas.extend(self._wrap_text(instruccion, self.fuente_pequena, max_texto_ancho))

        alto = 24 + self.fuente_normal.get_height() + len(lineas) * (self.fuente_pequena.get_height() + 4) + 16
        fondo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        fondo.fill((255, 255, 255, 220))
        self.pantalla.blit(fondo, (x, y))

        sombra_rect = pygame.Rect(x + 4, y + 4, ancho, alto)
        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 35))
        self.pantalla.blit(sombra, (x + 4, y + 4))

        rect = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(self.pantalla, (200, 180, 140), rect, 2, border_radius=20)

        titulo = self.fuente_normal.render("INSTRUCCIONES", True, (50, 45, 35))
        self.pantalla.blit(titulo, (x + 18, y + 10))

        linea_y = y + 38
        for linea in lineas:
            texto = self.fuente_pequena.render(linea, True, (60, 55, 45))
            self.pantalla.blit(texto, (x + 18, linea_y))
            linea_y += self.fuente_pequena.get_height() + 4
    
    def _dibujar_monstruo(self, x, y):
        pygame.draw.ellipse(self.pantalla, (150, 255, 150), (x - 30, y - 25, 60, 50))
        pygame.draw.circle(self.pantalla, BLANCO, (x - 12, y - 15), 10)
        pygame.draw.circle(self.pantalla, BLANCO, (x + 12, y - 15), 10)
        pygame.draw.circle(self.pantalla, NEGRO, (x - 12, y - 15), 5)
        pygame.draw.circle(self.pantalla, NEGRO, (x + 12, y - 15), 5)
        pygame.draw.ellipse(self.pantalla, NEGRO, (x - 12, y + 2, 24, 12))
        pygame.draw.line(self.pantalla, (150, 255, 150), (x - 15, y - 45), (x - 25, y - 60), 5)
        pygame.draw.line(self.pantalla, (150, 255, 150), (x + 15, y - 45), (x + 25, y - 60), 5)
        texto = self.fuente_pequena.render(" ¡Huy!", True, (0, 0, 0))
        self.pantalla.blit(texto, (x - 35, y - 75))
    
    def _dibujar_chef_gif(self, x, y):
        pass
    
    def _dibujar_estrellas(self):
        tiempo = pygame.time.get_ticks() / 500
        for i in range(15):
            x = (i * 100 + tiempo * 50) % PANTALLA_ANCHO
            y = 50 + math.sin(i) * 20
            pygame.draw.circle(self.pantalla, DORADO, (int(x), int(y)), 4)
            pygame.draw.circle(self.pantalla, (255, 255, 150), (int(x), int(y)), 2)
    
    def dibujar(self):
        """Dibuja toda la pantalla - SIN EL MUÑECO DEL CHEF"""
        # Fondo
        if self.custom_entrance_image:
            self.pantalla.blit(self.custom_entrance_image, (0, 0))
        else:
            self.pantalla.blit(self.fondo, (0, 0))
        
        # GIF de pizza animado
        if self.pizza_frames:
            self._actualizar_animacion_pizza()
            self.pantalla.blit(self.pizza_frames[self.pizza_frame_index], self.pizza_gif_rect)
        
        # Globos
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
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO // 2, 20))
        sombra = self.fuente_titulo.render("¡AVENTURA EN LA PASTELERÍA!", True, (100, 80, 20))
        sombra_rect = sombra.get_rect(center=(PANTALLA_ANCHO // 2 + 3, 20))
        self.pantalla.blit(sombra, sombra_rect)
        self.pantalla.blit(titulo, titulo_rect)

        # Instrucciones
        self._dibujar_cuadro_instrucciones()

        # MUÑECO ELIMINADO - Ya no se dibuja al chef
        
        # Monstruo
        self._dibujar_monstruo(PANTALLA_ANCHO - 120, PANTALLA_ALTO - 180)
        
        # Burbuja de diálogo
        if self.mostrando_dialogo and self.dialogo_actual < len(self.dialogos):
            self._dibujar_burbuja_dialogo(self.dialogos[self.dialogo_actual], 690, PANTALLA_ALTO - 70)
        
        # Instrucción espacio
        if pygame.time.get_ticks() // 500 % 2 == 0:
            instruccion = self.fuente_normal.render(" PRESIONA ESPACIO ", True, (255, 100, 50))
            instruccion_rect = instruccion.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO - 60))
            
            fondo_rect = pygame.Rect(instruccion_rect.x - 15, instruccion_rect.y - 8, instruccion_rect.w + 30, instruccion_rect.h + 16)
            pygame.draw.rect(self.pantalla, (255, 255, 200), fondo_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, MARRON, fondo_rect, 3, border_radius=20)
            self.pantalla.blit(instruccion, instruccion_rect)
    
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