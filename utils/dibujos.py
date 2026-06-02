# utils/dibujos.py
import pygame
import math
from config import *

class DibujosTorta:
    """Dibuja objetos de pastelería variados: tortas, barras y galletas."""

    def dibujar(self, pantalla, rect, numerador, denominador, color, sabor, nombre):
        contenido = pygame.Rect(rect.x + 12, rect.y + 12, rect.w - 24, rect.h - 28)
        pygame.draw.rect(pantalla, (255, 250, 240), contenido, border_radius=22)
        pygame.draw.rect(pantalla, MARRON, contenido, 2, border_radius=22)

        brillo = pygame.Surface((contenido.w, contenido.h), pygame.SRCALPHA)
        pygame.draw.ellipse(brillo, (255, 255, 255, 45), (0, 0, contenido.w, contenido.h // 2))
        pantalla.blit(brillo, contenido.topleft)

        estilo = self._elegir_estilo(sabor, denominador)
        if estilo == "galleta":
            self._dibujar_galleta(pantalla, contenido, numerador, denominador, color)
        elif estilo == "barra":
            self._dibujar_barra(pantalla, contenido, numerador, denominador, color)
        elif estilo == "dona":
            self._dibujar_dona(pantalla, contenido, numerador, denominador, color)
        elif estilo == "cupcake":
            self._dibujar_cupcake(pantalla, contenido, numerador, denominador, color)
        elif estilo == "waffle":
            self._dibujar_waffle(pantalla, contenido, numerador, denominador, color)
        elif estilo == "kiwi":
            self._dibujar_kiwi(pantalla, contenido, numerador, denominador, color)
        else:
            self._dibujar_pastel(pantalla, contenido, numerador, denominador, color)

        self._dibujar_nombre(pantalla, rect, nombre)

    def _elegir_estilo(self, sabor, denominador):
        sabor = sabor.lower()
        if sabor in ("galleta", "cookie", "brownie", "oreo"):
            return "galleta"
        if sabor == "kiwi":
            return "kiwi"
        if sabor in ("chocolate", "cacao", "caramelo", "avellana", "vainilla"):
            return "cupcake"
        if denominador == 6:
            return "dona"
        if denominador == 8 and sabor in ("banana", "pera"):
            return "waffle"
        return "pastel"

    def _dibujar_nombre(self, pantalla, rect, nombre):
        fuente_nom = pygame.font.Font(None, max(10, int(rect.h * 0.11)))
        texto_nom = fuente_nom.render(nombre, True, (60, 40, 30))
        nom_rect = texto_nom.get_rect(center=(rect.x + rect.w // 2, rect.y + rect.h - 12))
        fondo_nom = pygame.Rect(nom_rect.x - 8, nom_rect.y - 4, nom_rect.w + 16, nom_rect.h + 8)
        pygame.draw.rect(pantalla, (255, 245, 230), fondo_nom, border_radius=10)
        pygame.draw.rect(pantalla, (150, 100, 60), fondo_nom, 1, border_radius=10)
        pantalla.blit(texto_nom, nom_rect)

    def _dibujar_pastel(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        radio = int(min(rect.w, rect.h) * 0.34)
        plato = pygame.Rect(cx - radio - 14, cy - radio // 3, radio * 2 + 28, radio + 24)
        pygame.draw.ellipse(pantalla, (250, 250, 245), plato)
        pygame.draw.ellipse(pantalla, (210, 190, 165), plato, 3)

        base_color = self._tono(color, 0.9)
        borde_color = self._tono(color, 0.55)
        for capa in range(3):
            radio_capa = radio - capa * int(radio * 0.11)
            color_capa = self._tono(base_color, 1 - capa * 0.07)
            pygame.draw.circle(pantalla, color_capa, (cx, cy + capa * 4), radio_capa)
            pygame.draw.circle(pantalla, (190, 155, 110), (cx, cy + capa * 4), radio_capa, 2)
        pygame.draw.circle(pantalla, borde_color, (cx, cy), radio, 5)

        if denominador > 0:
            angulo_parte = 360 / denominador
            for i in range(denominador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                puntos = [(cx, cy)]
                for paso in range(16):
                    angulo = inicio + (fin - inicio) * paso / 15
                    px = cx + radio * math.cos(angulo)
                    py = cy + radio * math.sin(angulo)
                    puntos.append((px, py))

                relleno = self._tono(color, 1.25) if i < numerador else (245, 232, 195)
                pygame.draw.polygon(pantalla, relleno, puntos)
                pygame.draw.polygon(pantalla, (125, 80, 45), puntos, 2)

            for i in range(denominador):
                angulo = math.radians(i * angulo_parte - 90)
                px = cx + radio * math.cos(angulo)
                py = cy + radio * math.sin(angulo)
                pygame.draw.line(pantalla, (125, 80, 45), (cx, cy), (px, py), 4)

        glaseado = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(glaseado, (255, 255, 255, 190), (radio, radio), int(radio * 0.72))
        pygame.draw.circle(glaseado, (0, 0, 0, 0), (radio, radio), int(radio * 0.46))
        pantalla.blit(glaseado, (cx - radio, cy - radio))

        for i in range(min(denominador, 8)):
            ang = math.radians((i + 0.5) * angulo_parte - 90)
            dist = radio * 0.62
            px = cx + dist * math.cos(ang)
            py = cy + dist * math.sin(ang)
            pygame.draw.circle(pantalla, (255, 230, 210), (int(px), int(py)), max(4, radio // 14))
            pygame.draw.circle(pantalla, (165, 95, 60), (int(px), int(py)), max(1, radio // 24))

    def _dibujar_kiwi(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        radio = int(min(rect.w, rect.h) * 0.32)
        piel = (80, 120, 55)
        carne = (155, 220, 110)
        centro = (235, 255, 170)

        pygame.draw.circle(pantalla, piel, (cx, cy), radio)
        pygame.draw.circle(pantalla, (120, 165, 75), (cx, cy), radio - 10)
        pygame.draw.circle(pantalla, carne, (cx, cy), radio - 18)
        pygame.draw.circle(pantalla, centro, (cx, cy), int(radio * 0.45))

        if denominador > 0:
            angulo_parte = 360 / denominador
            for i in range(denominador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                puntos = [(cx, cy)]
                for paso in range(16):
                    angulo = inicio + (fin - inicio) * paso / 15
                    px = cx + (radio - 18) * math.cos(angulo)
                    py = cy + (radio - 18) * math.sin(angulo)
                    puntos.append((px, py))

                relleno = (190, 250, 135) if i < numerador else (210, 235, 145)
                pygame.draw.polygon(pantalla, relleno, puntos)
                pygame.draw.polygon(pantalla, (95, 135, 55), puntos, 2)

            for i in range(denominador):
                angulo = math.radians(i * angulo_parte - 90)
                px = cx + (radio - 18) * math.cos(angulo)
                py = cy + (radio - 18) * math.sin(angulo)
                pygame.draw.line(pantalla, (95, 135, 55), (cx, cy), (px, py), 3)

        for j in range(14):
            ang = math.radians(j * 25)
            dist = radio * (0.45 + 0.13 * ((j % 3) / 2))
            px = int(cx + math.cos(ang) * dist)
            py = int(cy + math.sin(ang) * dist)
            pygame.draw.circle(pantalla, (45, 75, 35), (px, py), max(2, radio // 22))
            if j % 3 == 0:
                pygame.draw.circle(pantalla, (255, 255, 255), (px, py), max(1, radio // 30))

    def _dibujar_cupcake(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        ancho = int(rect.w * 0.7)
        alto_base = int(rect.h * 0.24)
        base_rect = pygame.Rect(cx - ancho // 2, rect.bottom - alto_base - 18, ancho, alto_base)
        pygame.draw.rect(pantalla, (150, 80, 45), base_rect, border_radius=12)
        pygame.draw.rect(pantalla, (225, 165, 110), base_rect.inflate(-10, -10), border_radius=10)
        pygame.draw.line(pantalla, (130, 70, 40), (base_rect.x + 8, base_rect.y + 6), (base_rect.right - 8, base_rect.y + 6), 3)
        pygame.draw.line(pantalla, (130, 70, 40), (base_rect.x + 8, base_rect.bottom - 6), (base_rect.right - 8, base_rect.bottom - 6), 3)

        frosting_radio = int(min(rect.w, rect.h) * 0.3)
        for anillo in range(4):
            radio_n = frosting_radio - anillo * int(frosting_radio * 0.14)
            color_n = self._tono((245, 215, 235), 1 - anillo * 0.05)
            pygame.draw.ellipse(pantalla, color_n, pygame.Rect(cx - radio_n, cy - radio_n + anillo * 6, radio_n * 2, int(radio_n * 1.2)))
        pygame.draw.ellipse(pantalla, (205, 150, 175), pygame.Rect(cx - frosting_radio, cy - frosting_radio, frosting_radio * 2, int(frosting_radio * 1.2)), 3)

        if denominador > 0:
            angulo_parte = 360 / denominador
            for i in range(denominador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                puntos = [(cx, cy)]
                for paso in range(16):
                    angulo = inicio + (fin - inicio) * paso / 15
                    px = cx + (frosting_radio * 0.88) * math.cos(angulo)
                    py = cy + (frosting_radio * 0.88) * math.sin(angulo)
                    puntos.append((px, py))

                relleno = self._tono(color, 1.18) if i < numerador else (250, 240, 240)
                pygame.draw.polygon(pantalla, relleno, puntos)
                pygame.draw.polygon(pantalla, (150, 95, 125), puntos, 2)

        for j in range(12):
            ang = math.radians(j * 30 - 90)
            distancia = frosting_radio * (0.45 + 0.08 * ((j % 3) / 2))
            px = int(cx + math.cos(ang) * distancia)
            py = int(cy + math.sin(ang) * distancia)
            pygame.draw.circle(pantalla, (255, 215, 225), (px, py), max(3, frosting_radio // 18))
            pygame.draw.circle(pantalla, (185, 90, 135), (px, py), max(1, frosting_radio // 30))

    def _dibujar_waffle(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        tam = int(min(rect.w, rect.h) * 0.62)
        waffle_rect = pygame.Rect(cx - tam // 2, cy - tam // 2, tam, tam)
        pygame.draw.rect(pantalla, (215, 155, 90), waffle_rect, border_radius=20)
        pygame.draw.rect(pantalla, (190, 120, 60), waffle_rect.inflate(-10, -10), border_radius=16)

        if denominador == 8:
            rows, cols = 2, 4
        elif denominador <= 4:
            rows, cols = 1, denominador
        else:
            cols = math.ceil(math.sqrt(denominador))
            rows = math.ceil(denominador / cols)
        cell_w = waffle_rect.w / cols
        cell_h = waffle_rect.h / rows
        for index in range(denominador):
            fila = index // cols
            col = index % cols
            area = pygame.Rect(
                int(waffle_rect.x + col * cell_w + 5),
                int(waffle_rect.y + fila * cell_h + 5),
                int(cell_w - 10),
                int(cell_h - 10)
            )
            llena = index < numerador
            relleno = self._tono(color, 1.15) if llena else (220, 170, 105)
            pygame.draw.rect(pantalla, relleno, area, border_radius=8)
            pygame.draw.rect(pantalla, (140, 90, 45), area, 2, border_radius=8)
            brillo = pygame.Surface((area.w, area.h), pygame.SRCALPHA)
            pygame.draw.rect(brillo, (255, 255, 255, 45), brillo.get_rect(), border_radius=8)
            pantalla.blit(brillo, area.topleft)

        for line in range(1, cols):
            x = waffle_rect.x + int(line * cell_w)
            pygame.draw.line(pantalla, (150, 90, 50), (x, waffle_rect.y + 8), (x, waffle_rect.bottom - 8), 4)
        for line in range(1, rows):
            y = waffle_rect.y + int(line * cell_h)
            pygame.draw.line(pantalla, (150, 90, 50), (waffle_rect.x + 8, y), (waffle_rect.right - 8, y), 4)

        mantequilla = pygame.Rect(cx - 12, cy - 6, 24, 12)
        pygame.draw.ellipse(pantalla, (255, 220, 120), mantequilla)
        pygame.draw.ellipse(pantalla, (205, 165, 90), mantequilla, 2)

    def _dibujar_dona(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        radio_ext = int(min(rect.w, rect.h) * 0.34)
        radio_int = int(radio_ext * 0.45)
        fondo = self._tono((242, 196, 130), 1.0)
        pygame.draw.circle(pantalla, fondo, (cx, cy), radio_ext)
        pygame.draw.circle(pantalla, (220, 170, 120), (cx, cy), radio_ext, 6)
        pygame.draw.circle(pantalla, (255, 245, 220), (cx, cy), radio_int)

        if denominador > 0:
            angulo_parte = 360 / denominador
            for i in range(denominador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                points = []
                for paso in range(12):
                    angulo = inicio + (fin - inicio) * paso / 11
                    x = cx + radio_ext * math.cos(angulo)
                    y = cy + radio_ext * math.sin(angulo)
                    points.append((x, y))
                for paso in range(11, -1, -1):
                    angulo = inicio + (fin - inicio) * paso / 11
                    x = cx + radio_int * math.cos(angulo)
                    y = cy + radio_int * math.sin(angulo)
                    points.append((x, y))

                if i < numerador:
                    relleno = self._tono(color, 1.25)
                    pygame.draw.polygon(pantalla, relleno, points)
                pygame.draw.polygon(pantalla, (130, 80, 40), points, 2)

        glaseado = pygame.Surface((radio_ext * 2, radio_ext * 2), pygame.SRCALPHA)
        pygame.draw.circle(glaseado, (*self._tono(color, 1.2), 180), (radio_ext, radio_ext), int(radio_ext * 0.75))
        pygame.draw.circle(glaseado, (0, 0, 0, 0), (radio_ext, radio_ext), radio_int)
        pantalla.blit(glaseado, (cx - radio_ext, cy - radio_ext))

        for i in range(12):
            ang = math.radians(i * 30 + 14)
            dist = radio_ext * (0.55 + 0.08 * ((i % 3) / 2))
            px = cx + int(math.cos(ang) * dist)
            py = cy + int(math.sin(ang) * dist)
            pygame.draw.circle(pantalla, (255, 245, 240), (px, py), max(3, radio_ext // 16))
            if i % 2 == 0:
                pygame.draw.circle(pantalla, (200, 120, 140), (px, py), max(1, radio_ext // 24))

    def _dibujar_barra(self, pantalla, rect, numerador, denominador, color):
        ancho = rect.w * 0.92
        alto = rect.h * 0.32
        bar_rect = pygame.Rect(int(rect.x + (rect.w - ancho) / 2), int(rect.y + rect.h * 0.22), int(ancho), int(alto))
        pygame.draw.rect(pantalla, (120, 70, 40), bar_rect, border_radius=18)
        surface_interior = bar_rect.inflate(-6, -8)
        pygame.draw.rect(pantalla, (210, 170, 110), surface_interior, border_radius=14)

        rows = 2 if denominador > 4 else 1
        cols = math.ceil(denominador / rows)
        padding = 8
        pieza_w = (bar_rect.w - padding * (cols + 1)) / cols
        pieza_h = (surface_interior.h - padding * (rows + 1)) / rows

        for idx in range(denominador):
            fila = idx // cols
            columna = idx % cols
            px = surface_interior.x + padding + columna * (pieza_w + padding)
            py = surface_interior.y + padding + fila * (pieza_h + padding)
            pieza = pygame.Rect(int(px), int(py), int(pieza_w), int(pieza_h))
            llena = idx < numerador
            color_base = self._tono(color, 1.12) if llena else (190, 140, 100)
            pygame.draw.rect(pantalla, color_base, pieza, border_radius=10)
            pygame.draw.rect(pantalla, (100, 65, 35), pieza, 2, border_radius=10)
            brillo = pygame.Surface((pieza.w, pieza.h), pygame.SRCALPHA)
            pygame.draw.rect(brillo, (255, 255, 255, 35), brillo.get_rect(), border_radius=10)
            pantalla.blit(brillo, pieza.topleft)
            pygame.draw.line(pantalla, (135, 85, 45), (pieza.x, pieza.bottom - 4), (pieza.right, pieza.bottom - 4), 2)

    def _dibujar_galleta(self, pantalla, rect, numerador, denominador, color):
        cx, cy = rect.center
        radio = int(min(rect.w, rect.h) * 0.34)
        pygame.draw.circle(pantalla, (244, 196, 136), (cx, cy), radio)
        pygame.draw.circle(pantalla, (176, 115, 48), (cx, cy), radio, 3)

        mordida = pygame.Rect(cx + radio // 4, cy - radio // 2, radio * 2 // 3, radio * 2 // 3)
        pygame.draw.circle(pantalla, (255, 250, 240), mordida.center, mordida.w // 2)

        for i in range(12):
            ang = math.radians(i * 30 + 10)
            rchip = int(radio * 0.12)
            px = cx + int(math.cos(ang) * radio * 0.55)
            py = cy + int(math.sin(ang) * radio * 0.55)
            pygame.draw.circle(pantalla, (115, 65, 35), (px, py), rchip)

        if denominador > 0:
            angulo_parte = 360 / denominador
            for i in range(denominador):
                inicio = math.radians(i * angulo_parte - 90)
                fin = math.radians((i + 1) * angulo_parte - 90)
                puntos = [
                    (cx, cy),
                    (cx + radio * math.cos(inicio), cy + radio * math.sin(inicio)),
                    (cx + radio * math.cos(fin), cy + radio * math.sin(fin)),
                ]
                if i < numerador:
                    overlay = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                    pygame.draw.polygon(overlay, (*self._tono(color, 1.08), 120), [
                        (p[0] - rect.x, p[1] - rect.y) for p in puntos])
                    pantalla.blit(overlay, rect.topleft)
                pygame.draw.line(pantalla, (130, 75, 35), (cx, cy), puntos[1], 2)
                pygame.draw.line(pantalla, (130, 75, 35), (cx, cy), puntos[2], 2)

    def _tono(self, color, factor):
        return tuple(min(255, max(0, int(c * factor))) for c in color)