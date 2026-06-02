import pygame
import os
from PIL import Image

pygame.init()
pantalla = pygame.display.set_mode((800, 600))

# Verificar si existe el archivo
gif_path = "assets/pizza.gif"
if os.path.exists(gif_path):
    print(f"✅ Archivo encontrado: {gif_path}")
    
    # Intentar cargar con Pillow
    try:
        pil_img = Image.open(gif_path)
        print(f"✅ GIF cargado con Pillow")
        print(f"   - Dimensiones: {pil_img.size}")
        print(f"   - Formato: {pil_img.format}")
        print(f"   - Modo: {pil_img.mode}")
        print(f"   - Número de frames: {pil_img.n_frames}")
        
        # Extraer frames
        frames = []
        for i in range(pil_img.n_frames):
            pil_img.seek(i)
            # Convertir a pygame surface
            modo = pil_img.mode
            tamaño = pil_img.size
            datos = pil_img.tobytes()
            
            if modo == 'RGBA':
                formato = 'RGBA'
            elif modo == 'RGB':
                formato = 'RGB'
            else:
                # Convertir a RGB si es necesario
                pil_img = pil_img.convert('RGB')
                datos = pil_img.tobytes()
                formato = 'RGB'
            
            frame = pygame.image.fromstring(datos, tamaño, formato)
            frames.append(frame)
        
        print(f"✅ Extraídos {len(frames)} frames")
        
        # Mostrar animación
        reloj = pygame.time.Clock()
        frame_index = 0
        corriendo = True
        
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
            
            pantalla.fill((0, 0, 0))
            pantalla.blit(frames[frame_index], (300, 200))
            pygame.display.flip()
            
            frame_index = (frame_index + 1) % len(frames)
            reloj.tick(10)  # 10 fps para prueba
            
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print(f"❌ No se encontró el archivo: {gif_path}")
    print("Directorio actual:", os.getcwd())
    print("Archivos en assets:", os.listdir("assets") if os.path.exists("assets") else "carpeta assets no existe")

pygame.quit()