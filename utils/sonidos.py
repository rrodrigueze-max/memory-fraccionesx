# utils/sonidos.py
import pygame
import math

class GestorSonidos:
    """Gestiona todos los sonidos del juego"""
    
    def __init__(self):
        self.sonido_acierto = None
        self.sonido_error = None
        self.sonido_nivel = None
        self.sonido_victoria = None
        self._cargar_sonidos()
    
    def _cargar_sonidos(self):
        """Crea los sonidos usando pygame"""
        try:
            # Inicializar mixer si no está inicializado
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            self.sonido_acierto = self._crear_sonido_simple(523, 0.15)   # Do
            self.sonido_error = self._crear_sonido_simple(349, 0.25)     # Fa
            self.sonido_nivel = self._crear_sonido_simple(659, 0.3)      # Mi
            self.sonido_victoria = self._crear_sonido_simple(784, 0.5)   # Sol
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
            self._inicializar_sin_sonido()
    
    def _crear_sonido_simple(self, frecuencia, duracion):
        """Crea un sonido beep simple usando pygame"""
        try:
            sample_rate = 44100
            frames = int(duracion * sample_rate)
            
            # Crear datos de audio
            audio_data = bytearray()
            for i in range(frames):
                t = i / sample_rate
                # Onda sinusoidal
                valor = int(32767 * 0.5 * math.sin(2 * math.pi * frecuencia * t))
                # Envelope (fade in/out)
                if t < 0.05:
                    fade = t / 0.05
                    valor = int(valor * fade)
                elif t > duracion - 0.1:
                    fade = (duracion - t) / 0.1
                    valor = int(valor * fade)
                
                # Convertir a bytes (16-bit little endian)
                audio_data.extend(valor.to_bytes(2, 'little', signed=True))
                audio_data.extend(valor.to_bytes(2, 'little', signed=True))
            
            # Crear sonido
            sound = pygame.mixer.Sound(buffer=bytes(audio_data))
            return sound
        except Exception as e:
            print(f"Error creando sonido: {e}")
            return None
    
    def _inicializar_sin_sonido(self):
        """Inicializa sonidos nulos si hay error"""
        self.sonido_acierto = self.sonido_error = self.sonido_nivel = self.sonido_victoria = None
        print("Sonidos deshabilitados (modo silencioso)")
    
    def acierto(self):
        if self.sonido_acierto:
            try:
                self.sonido_acierto.play()
            except:
                pass
    
    def error(self):
        if self.sonido_error:
            try:
                self.sonido_error.play()
            except:
                pass
    
    def nivel_completado(self):
        if self.sonido_nivel:
            try:
                self.sonido_nivel.play()
            except:
                pass
    
    def victoria(self):
        if self.sonido_victoria:
            try:
                self.sonido_victoria.play()
            except:
                pass