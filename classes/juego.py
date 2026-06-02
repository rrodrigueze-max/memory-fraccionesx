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
        self.boton_pausa_rect = None
        # Contador de intentos (se incrementa cuando se abren dos cartas que no coinciden)
        self.intentos = 0
        
        # Gestores
        self.gestor_sonidos = GestorSonidos()
        self.gestor_fracciones = GestorFracciones()
        
        # Efectos visuales
        self.particulas = []
        self.estrellas = []
        self.confeti = []
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 52)
        self.fuente_info = pygame.font.Font(None, 30)
        self.fuente_grande = pygame.font.Font(None, 42)
        self.fuente_pequena = pygame.font.Font(None, 24)
        self.animacion_frame = 0.0
        
        self.iniciar_nivel()
    
    def pausar_juego(self):
        """Pausa el juego - EL TIEMPO NO AVANZA"""
        
        # Guardar el tiempo actual para no perderlo
        tiempo_guardado = self.ultimo_tiempo
        
        # Fuentes para pausa
        fuente_pausa = pygame.font.Font(None, 80)
        fuente_info = pygame.font.Font(None, 36)
        
        overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        overlay.set_alpha(180)
        overlay.fill((50, 50, 80))
        
        en_pausa = True
        while en_pausa:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        en_pausa = False
                    if event.key == pygame.K_r:
                        self.reiniciar_juego()
                        return True
            
            # Dibujar el juego debajo
            self._dibujar_fondo()
            self._dibujar_ui()
            self._dibujar_cartas()
            self._dibujar_efectos()
            self._dibujar_pantallas_fin()
            
            # Overlay de pausa
            self.pantalla.blit(overlay, (0, 0))
            
            # Círculo central
            cx, cy = PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2
            pygame.draw.circle(self.pantalla, (255, 255, 255), (cx, cy), 100)
            pygame.draw.circle(self.pantalla, (100, 100, 150), (cx, cy), 100, 5)
            
            # Icono de pausa (dos barras)
            pygame.draw.rect(self.pantalla, (50, 50, 100), (cx - 35, cy - 40, 25, 80), border_radius=8)
            pygame.draw.rect(self.pantalla, (50, 50, 100), (cx + 10, cy - 40, 25, 80), border_radius=8)
            
            # Texto PAUSA
            texto = fuente_pausa.render("PAUSA", True, (255, 100, 50))
            texto_rect = texto.get_rect(center=(cx, cy + 80))
            self.pantalla.blit(texto, texto_rect)
            
            # Mensajes
            msg1 = fuente_info.render("¡El juego está detenido!", True, BLANCO)
            msg1_rect = msg1.get_rect(center=(cx, cy + 140))
            self.pantalla.blit(msg1, msg1_rect)
            
            msg2 = fuente_info.render("Presiona P para continuar", True, AMARILLO)
            msg2_rect = msg2.get_rect(center=(cx, cy + 180))
            self.pantalla.blit(msg2, msg2_rect)
            
            # Emojis decorativos
            fuente_emoji = pygame.font.Font(None, 50)
            emojis = ["🍰", "🍕", "🎮", "⭐", "🏆"]
            for i, emoji in enumerate(emojis):
                texto_emoji = fuente_emoji.render(emoji, True, DORADO)
                x = cx - 180 + i * 90
                y = cy - 120
                self.pantalla.blit(texto_emoji, (x, y))
            
            pygame.display.flip()
            self.reloj.tick(30)
        
        # Restaurar el tiempo para que no haya pasado nada
        self.ultimo_tiempo = tiempo_guardado
        return True
    
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
        """Calcula y asigna posiciones a las cartas - CENTRADO PERFECTO"""
        
        # Configuración según nivel
        if filas == 2 and columnas == 2:  # Nivel 1 (2x2)
            espacio = 20
            margen_superior = 200
            ancho_carta = 160
            alto_carta = 150
        elif filas == 2 and columnas == 4:  # Nivel 2 (2x4)
            espacio = 15
            margen_superior = 200
            ancho_carta = 150
            alto_carta = 140
        else:  # Nivel 3 (4x4)
            espacio = 12
            margen_superior = 185
            ancho_carta = 115
            alto_carta = 110
        
        # Centrar el tablero
        ancho_total = columnas * ancho_carta + (columnas - 1) * espacio
        alto_total = filas * alto_carta + (filas - 1) * espacio
        margen_x = (PANTALLA_ANCHO - ancho_total) // 2
        margen_y = margen_superior
        
        # Posicionar cada carta
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reiniciar_juego()
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:  # Tecla P o ESPACIO para pausar
                    self.pausar_juego()
        return True
    
    def _manejar_click(self, pos):
        """Maneja los clics del mouse"""
        if self.boton_reset_rect and self.boton_reset_rect.collidepoint(pos):
            self.reiniciar_juego()
        elif self.boton_pausa_rect and self.boton_pausa_rect.collidepoint(pos):
            self.pausar_juego()
        elif self.esperando_siguiente_nivel and self.boton_continuar_rect and self.boton_continuar_rect.collidepoint(pos):
            self.siguiente_nivel()
            self.esperando_siguiente_nivel = False
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
            carta1.emparejada = True
            carta2.emparejada = True
            self.puntaje += 10
            self.parejas_encontradas += 1
            
            self._crear_efectos_celebracion(carta1.rect.center)
            self._crear_efectos_celebracion(carta2.rect.center)
            
            self.seleccionada1 = None
            self.seleccionada2 = None
            # Si se completaron todas las parejas, avanzar o terminar el juego
            if self.parejas_encontradas == self.total_parejas:
                max_nivel = max(NIVELES_CONFIG.keys()) if 'NIVELES_CONFIG' in globals() else 3
                if self.nivel_actual < max_nivel:
                    self.esperando_siguiente_nivel = True
                else:
                    # Último nivel completado -> mostrar pantalla de victoria
                    self.juego_terminado = True
                    self.victoria = True
        else:
            # Error
            # Incrementar intentos cuando fallan (los dos se abrieron y no emparejan)
            self.intentos += 1
            self.esperando = True
            self.tiempo_espera = pygame.time.get_ticks()
    
    def _crear_efectos_celebracion(self, pos):
        """Crea partículas y estrellas de celebración"""
        for _ in range(10):
            self.particulas.append(Particula(pos, random.choice([VERDE_CLARO, AMARILLO, DORADO, ROSA, MENTA])))
        for _ in range(4):
            self.estrellas.append(Estrella(pos))
    
    def siguiente_nivel(self):
        """Avanza al siguiente nivel"""
        if self.nivel_actual < 3:
            self.nivel_actual += 1
            self.iniciar_nivel()
        else:
            self.juego_terminado = True
            self.victoria = True
    
    def reiniciar_juego(self):
        """Reinicia completamente el juego"""
        self.nivel_actual = 1
        self.puntaje = 0
        self.intentos = 0
        self.gestor_fracciones.reiniciar_historial()
        self.esperando_siguiente_nivel = False
        self.confeti.clear()
        self.iniciar_nivel()
    
    def actualizar(self):
        """Actualiza el estado del juego"""
        if self.esperando and not self.juego_terminado:
            if pygame.time.get_ticks() - self.tiempo_espera > 800:
                if self.seleccionada1 is not None:
                    self.cartas[self.seleccionada1].visible = False
                if self.seleccionada2 is not None:
                    self.cartas[self.seleccionada2].visible = False
                self.seleccionada1 = None
                self.seleccionada2 = None
                self.esperando = False
        
        if not self.juego_terminado and not self.esperando and not self.esperando_siguiente_nivel:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_tiempo >= 1000:
                self.tiempo_restante -= 1
                self.ultimo_tiempo = ahora
                if self.tiempo_restante <= 0:
                    self.juego_terminado = True
                    self.victoria = False
        
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
        
        # Sol sonriente
        pygame.draw.circle(self.pantalla, DORADO, (70, 70), 32)
        pygame.draw.circle(self.pantalla, NEGRO, (58, 62), 3)
        pygame.draw.circle(self.pantalla, NEGRO, (82, 62), 3)
        pygame.draw.arc(self.pantalla, NEGRO, (55, 65, 30, 18), 0, math.pi, 2)
    
    def _dibujar_ui(self):
        """Dibuja la interfaz de usuario"""
        titulo = self.fuente_titulo.render("🍰 MEMORY de FRACCIONES 🎂", True, DORADO)
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO//2, 38))
        self.pantalla.blit(titulo, titulo_rect)
        
        subtitulo = self.fuente_pequena.render("¡Encuentra cada fracción con su torta!", True, BLANCO)
        subtitulo_rect = subtitulo.get_rect(center=(PANTALLA_ANCHO//2, 70))
        self.pantalla.blit(subtitulo, subtitulo_rect)
        
        panel_rect = pygame.Rect(20, 95, PANTALLA_ANCHO - 40, 55)
        pygame.draw.rect(self.pantalla, (50, 45, 65, 200), panel_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, DORADO, panel_rect, 2, border_radius=20)
        
        nivel_config = NIVELES_CONFIG[self.nivel_actual]
        
        texto_nivel = self.fuente_pequena.render(f"📚 {nivel_config['nombre']}", True, nivel_config["color"])
        self.pantalla.blit(texto_nivel, (35, 110))
        
        texto_tamano = self.fuente_pequena.render(f"🎲 {nivel_config['filas']}x{nivel_config['columnas']}", True, BLANCO)
        self.pantalla.blit(texto_tamano, (35, 132))
        
        texto_puntaje = self.fuente_pequena.render(f"⭐ {self.puntaje}", True, DORADO)
        puntaje_x = PANTALLA_ANCHO//2 - 60
        self.pantalla.blit(texto_puntaje, (puntaje_x, 110))
        
        texto_progreso = self.fuente_pequena.render(f"🎯 {self.parejas_encontradas}/{self.total_parejas}", True, BLANCO)
        self.pantalla.blit(texto_progreso, (puntaje_x, 132))
        # Mostrar contador de intentos
        texto_intentos = self.fuente_pequena.render(f"🧠 Intentos: {self.intentos}", True, BLANCO)
        self.pantalla.blit(texto_intentos, (puntaje_x + 140, 110))
        
        color_tiempo = VERDE if self.tiempo_restante > 20 else (AMARILLO if self.tiempo_restante > 10 else ROJO)
        texto_tiempo = self.fuente_pequena.render(f"⏰ {self.tiempo_restante}s", True, color_tiempo)
        tiempo_x = PANTALLA_ANCHO - 85
        self.pantalla.blit(texto_tiempo, (tiempo_x, 120))
        
        tiempo_max = nivel_config["tiempo"]
        barra_w = (PANTALLA_ANCHO - 100) * (self.tiempo_restante / tiempo_max)
        barra_x = 50
        barra_y = 170
        pygame.draw.rect(self.pantalla, (60, 55, 75), (barra_x, barra_y, PANTALLA_ANCHO - 100, 8), border_radius=4)
        pygame.draw.rect(self.pantalla, color_tiempo, (barra_x, barra_y, max(0, barra_w), 8), border_radius=4)
        
        self.boton_reset_rect = pygame.Rect(PANTALLA_ANCHO - 100, 105, 75, 35)
        pygame.draw.rect(self.pantalla, NARANJA, self.boton_reset_rect, border_radius=18)
        pygame.draw.rect(self.pantalla, DORADO, self.boton_reset_rect, 2, border_radius=18)
        texto_reset = self.fuente_pequena.render("🔄", True, BLANCO)
        texto_reset_rect = texto_reset.get_rect(center=self.boton_reset_rect.center)
        self.pantalla.blit(texto_reset, texto_reset_rect)
        # Botón de pausa (para niños: grande y claro)
        self.boton_pausa_rect = pygame.Rect(PANTALLA_ANCHO - 190, 105, 75, 35)
        pygame.draw.rect(self.pantalla, AZUL_CLARO, self.boton_pausa_rect, border_radius=18)
        pygame.draw.rect(self.pantalla, DORADO, self.boton_pausa_rect, 2, border_radius=18)
        texto_pausa_icon = self.fuente_pequena.render("⏸", True, BLANCO)
        texto_pausa_icon_rect = texto_pausa_icon.get_rect(center=self.boton_pausa_rect.center)
        self.pantalla.blit(texto_pausa_icon, texto_pausa_icon_rect)
        # Pista para pausar con la tecla ESPACIO
        texto_pausa_pista = self.fuente_pequena.render("Presiona ESPACIO para pausar", True, BLANCO)
        pista_rect = texto_pausa_pista.get_rect()
        pista_rect.topright = (PANTALLA_ANCHO - 120, 152)
        self.pantalla.blit(texto_pausa_pista, pista_rect)
    
    def _dibujar_cartas(self):
        """Dibuja todas las cartas"""
        for carta in self.cartas:
            carta.dibujar(self.pantalla)

    def _dibujar_efectos(self):
        """Dibuja los efectos visuales"""
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
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 50))
        self.pantalla.blit(texto, texto_rect)
        
        puntos_texto = self.fuente_info.render(f"🍰 Puntos: {self.puntaje} 🍰", True, BLANCO)
        puntos_rect = puntos_texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2))
        self.pantalla.blit(puntos_texto, puntos_rect)
        # Mostrar intentos en pantalla de nivel completado
        intentos_text = self.fuente_info.render(f"Intentos: {self.intentos}", True, BLANCO)
        intentos_rect = intentos_text.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 30))
        self.pantalla.blit(intentos_text, intentos_rect)
        
        self.boton_continuar_rect = pygame.Rect(PANTALLA_ANCHO//2 - 110, PANTALLA_ALTO//2 + 50, 220, 45)
        pygame.draw.rect(self.pantalla, VERDE, self.boton_continuar_rect, border_radius=25)
        pygame.draw.rect(self.pantalla, DORADO, self.boton_continuar_rect, 3, border_radius=25)
        texto_cont = self.fuente_info.render("🎂 SIGUIENTE NIVEL 🎂", True, BLANCO)
        texto_cont_rect = texto_cont.get_rect(center=self.boton_continuar_rect.center)
        self.pantalla.blit(texto_cont, texto_cont_rect)
    
    def _dibujar_chef_con_recetas(self, x, y):
        self.animacion_frame += 0.08
        salto = int(math.sin(self.animacion_frame) * 4)

        # Cuerpo y camisa de chef
        pygame.draw.ellipse(self.pantalla, BLANCO, (x - 50, y - 60 + salto, 100, 130))
        pygame.draw.rect(self.pantalla, (240, 240, 240), (x - 45, y - 10 + salto, 90, 80), border_radius=20)
        pygame.draw.rect(self.pantalla, (255, 230, 190), (x - 28, y + 20 + salto, 56, 20), border_radius=12)
        pygame.draw.circle(self.pantalla, (220, 220, 220), (x - 15, y + 10 + salto), 6)
        pygame.draw.circle(self.pantalla, (220, 220, 220), (x + 15, y + 10 + salto), 6)

        # Piernas y zapatos
        pygame.draw.line(self.pantalla, (200, 200, 200), (x - 25, y + 70 + salto), (x - 30, y + 110 + salto), 12)
        pygame.draw.line(self.pantalla, (200, 200, 200), (x + 25, y + 70 + salto), (x + 30, y + 110 + salto), 12)
        pygame.draw.ellipse(self.pantalla, (100, 160, 220), (x - 34, y + 105 + salto, 24, 14))
        pygame.draw.ellipse(self.pantalla, (100, 160, 220), (x + 10, y + 105 + salto, 24, 14))

        # Cabeza y gorro
        pygame.draw.circle(self.pantalla, (255, 220, 160), (x, y - 20 + salto), 42)
        pygame.draw.circle(self.pantalla, BLANCO, (x - 15, y - 30 + salto), 12)
        pygame.draw.circle(self.pantalla, BLANCO, (x + 15, y - 30 + salto), 12)
        pygame.draw.circle(self.pantalla, NEGRO, (x - 15, y - 30 + salto), 6)
        pygame.draw.circle(self.pantalla, NEGRO, (x + 15, y - 30 + salto), 6)
        pygame.draw.polygon(self.pantalla, (255, 200, 170), [(x, y - 21 + salto), (x - 8, y - 10 + salto), (x + 8, y - 10 + salto)])
        pygame.draw.arc(self.pantalla, NEGRO, (x - 20, y - 8 + salto, 40, 24), 0, math.pi, 4)
        pygame.draw.rect(self.pantalla, BLANCO, (x - 35, y - 60 + salto, 70, 26), border_radius=10)
        pygame.draw.ellipse(self.pantalla, BLANCO, (x - 28, y - 85 + salto, 56, 40))

        # Brazos y recetas
        pygame.draw.line(self.pantalla, (255, 220, 160), (x - 35, y + 10 + salto), (x - 75, y + 30 + salto), 14)
        pygame.draw.line(self.pantalla, (255, 220, 160), (x + 35, y + 10 + salto), (x + 75, y + 26 + salto), 14)
        pygame.draw.circle(self.pantalla, (255, 220, 160), (x - 75, y + 30 + salto), 10)
        pygame.draw.circle(self.pantalla, (255, 220, 160), (x + 75, y + 26 + salto), 10)

        receta_base = pygame.Rect(x + 60, y + 10 + salto, 38, 52)
        pygame.draw.rect(self.pantalla, (255, 250, 230), receta_base, border_radius=8)
        pygame.draw.rect(self.pantalla, (240, 230, 210), receta_base.inflate(-8, -8), border_radius=8)
        pygame.draw.line(self.pantalla, NEGRO, (receta_base.x + 8, receta_base.y + 14), (receta_base.x + 28, receta_base.y + 14), 2)
        pygame.draw.line(self.pantalla, NEGRO, (receta_base.x + 8, receta_base.y + 24), (receta_base.x + 28, receta_base.y + 24), 2)
        pygame.draw.line(self.pantalla, NEGRO, (receta_base.x + 8, receta_base.y + 34), (receta_base.x + 28, receta_base.y + 34), 2)

        carta2 = receta_base.move(-10, -8)
        pygame.draw.rect(self.pantalla, (255, 255, 255), carta2, border_radius=8)
        pygame.draw.rect(self.pantalla, (235, 230, 210), carta2.inflate(-8, -8), border_radius=8)

        carta3 = receta_base.move(-6, 8)
        pygame.draw.rect(self.pantalla, (255, 255, 255), carta3, border_radius=8)
        pygame.draw.rect(self.pantalla, (235, 230, 210), carta3.inflate(-8, -8), border_radius=8)

    def _dibujar_pantalla_victoria(self):
        """Pantalla de victoria final"""
        
        overlay = pygame.Surface((PANTALLA_ANCHO, PANTALLA_ALTO))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        
        for _ in range(100):
            x = random.randint(0, PANTALLA_ANCHO)
            y = random.randint(0, PANTALLA_ALTO)
            color = random.choice([ROJO, AMARILLO, VERDE, AZUL_CLARO, ROSA])
            pygame.draw.circle(self.pantalla, color, (x, y), random.randint(2, 5))
        
        titulo = self.fuente_grande.render("🎉 ¡FELICIDADES! 🎉", True, DORADO)
        titulo_rect = titulo.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 120))
        self.pantalla.blit(titulo, titulo_rect)
        
        self._dibujar_chef_con_recetas(PANTALLA_ANCHO//2, PANTALLA_ALTO - 180)
        
        texto1 = self.fuente_grande.render("🏆 COMPLETASTE TODOS LOS NIVELES 🏆", True, AMARILLO)
        texto1_rect = texto1.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 20))
        self.pantalla.blit(texto1, texto1_rect)
        
        puntos = self.fuente_info.render(f"⭐ PUNTUACIÓN FINAL: {self.puntaje} PUNTOS ⭐", True, BLANCO)
        puntos_rect = puntos.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 40))
        self.pantalla.blit(puntos, puntos_rect)
        
        gracias = self.fuente_info.render("🍰 ¡GRACIAS POR RECUPERAR LAS RECETAS! 🍰", True, (255, 200, 100))
        gracias_rect = gracias.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 90))
        self.pantalla.blit(gracias, gracias_rect)
        
        intentos = self.fuente_info.render(f"Intentos totales: {self.intentos}", True, BLANCO)
        intentos_rect = intentos.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 60))
        self.pantalla.blit(intentos, intentos_rect)
        
        reinicio = self.fuente_pequena.render("PRESIONA R PARA VOLVER A JUGAR", True, BLANCO)
        reinicio_rect = reinicio.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 160))
        
        fondo_rect = pygame.Rect(reinicio_rect.x - 15, reinicio_rect.y - 8, reinicio_rect.w + 30, reinicio_rect.h + 16)
        pygame.draw.rect(self.pantalla, (60, 50, 70), fondo_rect, border_radius=15)
        pygame.draw.rect(self.pantalla, DORADO, fondo_rect, 2, border_radius=15)
        self.pantalla.blit(reinicio, reinicio_rect)
        
        pygame.display.flip()
        
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        esperando = False
                        self.reiniciar_juego()
                    elif event.key == pygame.K_ESCAPE:
                        esperando = False
    
    def _dibujar_pantalla_derrota(self):
        """Pantalla de derrota por tiempo"""
        texto = self.fuente_grande.render("😢 ¡SE ACABÓ EL TIEMPO! 😢", True, ROJO_CLARO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 - 50))
        self.pantalla.blit(texto, texto_rect)
        
        resultado = self.fuente_info.render(f"Completaste {self.parejas_encontradas} de {self.total_parejas} parejas", True, BLANCO)
        resultado_rect = resultado.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2))
        self.pantalla.blit(resultado, resultado_rect)
        
        reinicio = self.fuente_info.render("Presiona R para reiniciar el juego", True, AMARILLO)
        reinicio_rect = reinicio.get_rect(center=(PANTALLA_ANCHO//2, PANTALLA_ALTO//2 + 60))
        self.pantalla.blit(reinicio, reinicio_rect)