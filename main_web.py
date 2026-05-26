# main_web.py - Punto de entrada para la web
import asyncio
from classes.juego import JuegoMemory
import pygame

async def main():
    pygame.init()
    pygame.mixer.init()
    
    # Crear pantalla
    pantalla = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("🍰 Memory de Fracciones")
    
    # Iniciar juego
    juego = JuegoMemory(pantalla)
    
    # Bucle principal asíncrono (necesario para pygbag)
    while True:
        corriendo = juego.manejar_eventos()
        juego.actualizar()
        juego.dibujar()
        await asyncio.sleep(0)
        juego.reloj.tick(60)
    
    pygame.quit()

asyncio.run(main())