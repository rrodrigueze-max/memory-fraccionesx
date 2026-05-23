# classes/juego.py
import pygame
import random
import math 
from config import *
from classes.tarjeta import Tarjeta
from classes.efectos import Particula, Estrella, Confeti
from utils.sonidos import GestorSonidos
from utils.fracciones import GestorFracciones

class JuegoMemory:
    """Clase principal del juego"""
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pygame.time.Clock()
        
        # Estado del juego
        self.nivel_actual = 1
        self.cartas = []
        self.seleccionada1 = None
        self.seleccionada2 = None
        self.esperando = False
        self.tiempo_espera = 0
        self.puntaje = 0
        self.tiempo_restante = 0
        self.juego_terminado = False
        self.victoria = False
        self.ultimo_tiempo = pygame.time.get_ticks()
        self.parejas_encontradas = 0
        self.total_parejas = 0
        self.esperando_siguiente_nivel = False
        self.boton_continuar_rect = None
        self.boton_reset_rect = None
        
        # Gestores
        self.gestor_sonidos = GestorSonidos()
        self.gestor_fracciones = GestorFracciones()
        
        # Efectos visuales
        self.particulas = []
        self.estrellas = []
        self.confeti = []
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 58)
        self.fuente_info = pygame.font.Font(None, 34)
        self.fuente_grande = pygame.font.Font(None, 46)
        
        self.iniciar_nivel()
    
    def iniciar_nivel(self):
        """Inicializa un nuevo nivel"""
        nivel_config = NIVELES_CONFIG[self.nivel_actual]
        filas = nivel_config["filas"]
        columnas = nivel_config["columnas"]
        pares = nivel_config["pares"]
        
        self.tiempo_restante = nivel_config["tiempo"]
        self.parejas_encontradas = 0
        self.total_parejas = pares
        self.seleccionada1 = None
        self.seleccionada2 = None
        self.esperando = False
        self.juego_terminado = False
        self.victoria = False
        self.esperando_siguiente_nivel = False
        self.particulas.clear()
        self.estrellas.clear()
        self.ultimo_tiempo = pygame.time.get_ticks()
        
        # Seleccionar fracciones para este nivel
        fracciones_usar = self.gestor_fracciones.seleccionar_aleatorias(pares)
        
        # Crear pares de cartas
        cartas_lista = []
        for i, frac in enumerate(fracciones_usar):
            _, tipo, num, den, color, emoji, nombre, sabor = frac
            cartas_lista.append(Tarjeta(i, "texto", num, den, color, emoji, nombre, sabor, 0, 0, 0, 0))
            cartas_lista.append(Tarjeta(i, "torta", num, den, color, emoji, nombre, sabor, 0, 0, 0, 0))
        
        random.shuffle(cartas_lista)
        
        # Posicionar cartas en el tablero
        self._posicionar_cartas(cartas_lista, filas, columnas)
        self.cartas = cartas_lista
    
    def _posicionar_cartas(self, cartas, filas, columnas):
        """Calcula y asigna posiciones a las cartas"""
        margen_x = 50
        margen_y = 180
        espacio = 15
        
        ancho_carta = (PANTALLA_ANCHO - 2 * margen_x - (columnas - 1) * espacio) // columnas
        alto_carta = (PANTALLA_ALTO - margen_y - 80 - (filas - 1) * espacio) // filas
        
        ancho_carta = min(ancho_carta, 180)
        alto_carta = min(alto_carta, 170)
        
        ancho_total = columnas * ancho_carta + (columnas - 1) * espacio
        alto_total = filas * alto_carta + (filas - 1) * espacio
        margen_x = (PANTALLA_ANCHO - ancho_total) // 2
        margen_y = (PANTALLA_ALTO - alto_total) // 2 + 50
        
        for idx, carta in enumerate(cartas):
            fila = idx // columnas
            columna = idx % columnas
            x = margen_x + columna * (ancho_carta + espacio)
            y = margen_y + fila * (alto_carta + espacio)
            carta.rect.x = x
            carta.rect.y = y
            carta.rect.w = ancho_carta
            carta.rect.h = alto_carta
            carta.visible = False
            carta.emparejada = False
    
    def manejar_eventos(self):
        """Maneja todos los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._manejar_click(pygame.mouse.get_pos())
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reiniciar_juego()
        
        return True
    
    def _manejar_click(self, pos):
        """Maneja los clics del mouse"""
        # Botón reiniciar
        if self.boton_reset_rect and self.boton_reset_rect.collidepoint(pos):
            self.reiniciar_juego()
        
        # Botón continuar
        elif self.esperando_siguiente_nivel and self.boton_continuar_rect and self.boton_continuar_rect.collidepoint(pos):
            self.siguiente_nivel()
            self.esperando_siguiente_nivel = False
        
        # Jugar normalmente
        elif not self.esperando and not self.juego_terminado and not self.esperando_siguiente_nivel:
            self._manejar_click_carta(pos)
    
    def _manejar_click_carta(self, pos):
        """Maneja el clic en una carta"""
        for i, carta in enumerate(self.cartas):
            if carta.rect.collidepoint(pos) and not carta.emparejada and not carta.visible:
                if self.seleccionada1 is None:
                    carta.visible = True
                    self.seleccionada1 = i
                elif self.seleccionada2 is None and i != self.seleccionada1:
                    carta.visible = True
                    self.seleccionada2 = i
                    self._verificar_pareja()
                break
    
    def _verificar_pareja(self):
        """Verifica si las dos cartas seleccionadas forman pareja"""
        carta1 = self.cartas[self.seleccionada1]
        carta2 = self.cartas[self.seleccionada2]
        
        if carta1.id_fraccion == carta2.id_fraccion:
            # Acierto
            self.gestor_sonidos.acierto()
            carta1.emparejada = True
            carta2.emparejada = True
            self.puntaje += PUNTOS_POR_PAREJA
            self.parejas_encontradas += 1
            
            self._crear_efectos_celebracion(carta1.rect.center)
            self._crear_efectos_celebracion(carta2.rect.center)
            
            self.seleccionada1 = None
            self.seleccionada2 = None
            
            if self.parejas_encontradas == self.total_parejas:
                self.esperando_siguiente_nivel = True
        else:
            # Error
            self.gestor_sonidos.error()
            self.esperando = True
            self.tiempo_espera = pygame.time.get_ticks()
    
    def _crear_efectos_celebracion(self, pos):
        """Crea partículas y estrellas de celebración"""
        for _ in range(15):
            self.particulas.append(Particula(pos, random.choice([VERDE_CLARO, AMARILLO, DORADO, ROSA, MENTA])))
        for _ in range(6):
            self.estrellas.append(Estrella(pos))
    
    def siguiente_nivel(self):
        """Avanza al siguiente nivel"""
        if self.nivel_actual < 3:
            self.gestor_sonidos.nivel_completado()
            self.nivel_actual += 1
            self.iniciar_nivel()
        else:
            self.gestor_sonidos.victoria()
            self.juego_terminado = True
            self.victoria = True
            # Crear confeti
            for _ in range(150):
                self.confeti.append(Confeti(PANTALLA_ANCHO))
    
    def reiniciar_juego(self):
        """Reinicia completamente el juego"""
        self.nivel_actual = 1
        self.puntaje = 0
        self.gestor_fracciones.reiniciar_historial()
        self.esperando_siguiente_nivel = False
        self.confeti.clear()
        self.iniciar_nivel()
    
    def actualizar(self):
        """Actualiza el estado del juego"""
        # Manejar espera después de error
        if self.esperando and not self.juego_terminado:
            if pygame.time.get_ticks() - self.tiempo_espera > TIEMPO_ESPERA_ERROR:
                if self.seleccionada1 is not None:
                    self.cartas[self.seleccionada1].visible = False
                if self.seleccionada2 is not None:
                    self.cartas[self.seleccionada2].visible = False
                self.seleccionada1 = None
                self.seleccionada2 = None
                self.esperando = False
        
        # Actualizar tiempo
        if not self.juego_terminado and not self.esperando and not self.esperando_siguiente_nivel:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_tiempo >= 1000:
                self.tiempo_restante -= 1
                self.ultimo_tiempo = ahora
                if self.tiempo_restante <= 0:
                    self.juego_terminado = True
                    self.victoria = False
        
        # Actualizar efectos visuales
        self.particulas = [p for p in self.particulas if p.actualizar()]
        self.estrellas = [e for e in self.estrellas if e.actualizar()]
        self.confeti = [c for c in self.confeti if c.actualizar()]
    
    def dibujar(self):
        """Dibuja todos los elementos en pantalla"""
        self._dibujar_fondo()
        self._dibujar_ui()
        self._dibujar_cartas()
        self._dibujar_efectos()
        self._dibujar_pantallas_fin()
        pygame.display.flip()
    
    def _dibujar_fondo(self):
        """Dibuja el fondo del juego"""
        for y in range(PANTALLA_ALTO):
            if y < PANTALLA_ALTO // 2:
                t = y / (PANTALLA_ALTO // 2)
                r = int(135 + (70 - 135) * t)
                g = int(206 + (50 - 206) * t)
                b = int(235 + (70 - 235) * t)
            else:
                t = (y - PANTALLA_ALTO // 2) / (PANTALLA_ALTO // 2)
                r = int(70 + (30 - 70) * t)
                g = int(50 + (40 - 50) * t)
                b = int(70 + (50 - 70) * t)
            pygame.draw.line(self.pantalla, (r, g, b), (0, y), (PANTALLA_ANCHO, y))
        
        # Nubes
        tiempo = pygame.time.get_ticks() // 60
        nubes = [
            (80 + tiempo % 800, 60, 100, 55),
            (350 + (tiempo * 0.7) % 900, 90, 85, 48),
            (650 + (tiempo * 1.2) % 600, 45, 110, 60),
        ]
        for nx, ny, w, h in nubes:
            pygame.draw.ellipse(self.pantalla, (255, 255, 255, 200), (nx, ny, w, h))
        
        # Sol sonriente
        pygame.draw.circle(self.pantalla, DORADO, (75, 75), 38)
        pygame.draw.circle(self.pantalla, NEGRO, (62, 67), 4)
        pygame.draw.circle(self.pantalla, NEGRO, (88, 67), 4)
        pygame.draw.arc(self.pantalla, NEGRO, (58, 70, 35, 22), 0, math.pi, 3)
    
    def _dibujar_ui(self):
        """Dibuja la interfaz de usuario"""
        # Título
        titulo = self.fuente_titulo.render("🍰 MEMORY de FRACCIONES 🎂", True, DORADO)
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO//2, 42))
        self.pantalla.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = self.fuente_info.render("¡Encuentra cada fracción con su TORTA DELICIOSA!", True, BLANCO)
        subtitulo_rect = subtitulo.get_rect(center=(PANTALLA_ANCHO//2, 80))
        self.pantalla.blit(subtitulo, subtitulo_rect)
        
        # Panel
        panel_rect = pygame.Rect(20, 110, PANTALLA_ANCHO - 40, 70)
        pygame.draw.rect(self.pantalla, (60, 50, 70, 200), panel_rect, border_radius=25)
        pygame.draw.rect(self.pantalla, DORADO, panel_rect, 3, border_radius=25)
        
        # Información
        nivel_config = NIVELES_CONFIG[self.nivel_actual]
        texto_nivel = self.fuente_info.render(f"📚 {nivel_config['nombre']}", True, nivel_config["color"])
        self.pantalla.blit(texto_nivel, (40, 125))
        
        texto_tamano = self.fuente_info.render(f"🎲 {nivel_config['filas']}x{nivel_config['columnas']}", True, BLANCO)
        self.pantalla.blit(texto_tamano, (40, 150))
        
        texto_puntaje = self.fuente_info.render(f"⭐ Puntos: {self.puntaje}", True, DORADO)
        self.pantalla.blit(texto_puntaje, (PANTALLA_ANCHO//2 - 100, 125))
        
        texto_progreso = self.fuente_info.render(f"🎯 Parejas: {self.parejas_encontradas}/{self.total_parejas}", True, BLANCO)
        self.pantalla.blit(texto_progreso, (PANTALLA_ANCHO//2 - 100, 150))
        
        # Tiempo
        color_tiempo = VERDE if self.tiempo_restante > 20 else (AMARILLO if self.tiempo_restante > 10 else ROJO)
        texto_tiempo = self.fuente_info.render(f"⏰ Tiempo: {self.tiempo_restante}", True, color_tiempo)
        tiempo_x = PANTALLA_ANCHO - texto_tiempo.get_width() - 50
        self.pantalla.blit(texto_tiempo, (tiempo_x, 135))
        
        # Barra de tiempo
        barra_w = (PANTALLA_ANCHO - 100) * (self.tiempo_restante / nivel_config["tiempo"])
        pygame.draw.rect(self.pantalla, (60, 60, 80), (50, 175, PANTALLA_ANCHO - 100, 12), border_radius=6)
        pygame.draw.rect(self.pantalla, color_tiempo, (50, 175, max(0, barra_w), 12), border_radius=6)
        
        # Botón reiniciar
        self.boton_reset_rect = pygame.Rect(PANTALLA_ANCHO - 110, 118, 90, 40)
        pygame.draw.rect(self.pantalla, NARANJA, self.boton_reset_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, DORADO, self.boton_reset_rect, 3, border_radius=20)
        texto_reset = self.fuente_info.render("🔄", True, BLANCO)
        texto_reset_rect = texto_reset.get_rect(center=self.boton_reset_rect.center)
        self.pantalla.blit(texto_reset, texto_reset_rect)
    
    def _dibujar_cartas(self):
        """Dibuja todas las cartas"""
        for carta in self.cartas:
            carta.dibujar(self.pantalla)
    
    def _dibujar_efectos(self):
        """Dibuja todos los efectos visuales"""
        for p in self.particulas:
            p.dibujar(self.pantalla)
        for e in self.estrellas:
            e.dibujar(self.pantalla)
        for c in self.confeti:
            c.dibujar(self.pantalla)
    
    def _dibujar_pantallas_fin(self):
        """Dibuja las pantallas de fin de nivel/juego"""
        if self.esperando_siguiente_nivel:
            overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            self.pantalla.blit(overlay, (0, 0))
            
            if self.nivel_actual < 3:
                self._dibujar_pantalla_nivel_completado()
        
        elif self.juego_terminado:
            overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            self.pantalla.blit(overlay, (0, 0))
            
            if self.victoria:
                self._dibujar_pantalla_victoria()
            else:
                self._dibujar_pantalla_derrota()
    
    def _dibujar_pantalla_nivel_completado(self):
        """Pantalla de nivel completado"""
        texto = self.fuente_grande.render(f"🎉 ¡NIVEL {self.nivel_actual} COMPLETADO! 🎉", True, DORADO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 60))
        self.pantalla.blit(texto, texto_rect)
        
        puntos_texto = self.fuente_info.render(f"🍰 Puntos: {self.puntaje} puntos 🍰", True, BLANCO)
        puntos_rect = puntos_texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2))
        self.pantalla.blit(puntos_texto, puntos_rect)
        
        self.boton_continuar_rect = pygame.Rect(PANTALLA_ANCHO//2 - 130, PANTALLA_ALTO//2 + 60, 260, 55)
        pygame.draw.rect(self.pantalla, VERDE, self.boton_continuar_rect, border_radius=28)
        pygame.draw.rect(self.pantalla, DORADO, self.boton_continuar_rect, 4, border_radius=28)
        texto_cont = self.fuente_grande.render("🎂 SIGUIENTE NIVEL 🎂", True, BLANCO)
        texto_cont_rect = texto_cont.get_rect(center=self.boton_continuar_rect.center)
        self.pantalla.blit(texto_cont, texto_cont_rect)
    
    def _dibujar_pantalla_victoria(self):
        """Pantalla de victoria final"""
        texto = self.fuente_grande.render("🏆 ¡COMPLETASTE EL JUEGO! 🏆", True, DORADO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 60))
        self.pantalla.blit(texto, texto_rect)
        
        puntos = self.fuente_info.render(f"⭐ Puntuación final: {self.puntaje} puntos ⭐", True, AMARILLO)
        puntos_rect = puntos.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2))
        self.pantalla.blit(puntos, puntos_rect)
        
        reinicio = self.fuente_info.render("Presiona R para volver a jugar", True, BLANCO)
        reinicio_rect = reinicio.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 80))
        self.pantalla.blit(reinicio, reinicio_rect)
    
    def _dibujar_pantalla_derrota(self):
        """Pantalla de derrota por tiempo"""
        texto = self.fuente_grande.render("😢 ¡SE ACABÓ EL TIEMPO! 😢", True, ROJO_CLARO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 60))
        self.pantalla.blit(texto, texto_rect)
        
        resultado = self.fuente_info.render(f"Completaste {self.parejas_encontradas} de {self.total_parejas} parejas", True, BLANCO)
        resultado_rect = resultado.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2))
        self.pantalla.blit(resultado, resultado_rect)
        
        reinicio = self.fuente_info.render("Presiona R para reiniciar el juego", True, AMARILLO)
        reinicio_rect = reinicio.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 80))
        self.pantalla.blit(reinicio, reinicio_rect)
        