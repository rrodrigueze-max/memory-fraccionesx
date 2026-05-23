# main.py
import pygame
import sys
from classes.juego import JuegoMemory
from config import PANTALLA_ANCHO, PANTALLA_ALTO


def main():
    """Punto de entrada principal del juego"""
    # Inicializar Pygame
    pygame.init()
    
    # Inicializar mixer para sonido
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    except:
        print("No se pudo inicializar el sonido")
    
    # Crear pantalla
    pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
    pygame.display.set_caption("🍰 Memory de Fracciones - ¡Aprende con Tortas! 🎂")
    
    # Crear e iniciar el juego
    juego = JuegoMemory(pantalla)
    
    # Bucle principal
    corriendo = True
    while corriendo:
        corriendo = juego.manejar_eventos()
        juego.actualizar()
        juego.dibujar()
        juego.reloj.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()