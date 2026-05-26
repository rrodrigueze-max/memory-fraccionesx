# utils/fracciones.py
import random  # ← ESTA LÍNEA FALTABA

"""
Banco de fracciones con información de cada torta
"""

BANCO_FRACCIONES = [
    # (texto, tipo, numerador, denominador, color, emoji, nombre, sabor)
    ("1/2", "torta", 1, 2, (255, 100, 100), "🍰", "Torta de Fresa", "fresa"),
    ("1/3", "torta", 1, 3, (100, 255, 100), "🍎", "Tarta de Manzana", "manzana"),
    ("2/3", "torta", 2, 3, (100, 150, 255), "🫐", "Pastel de Arándanos", "arandano"),
    ("1/4", "torta", 1, 4, (255, 200, 100), "🍋", "Tarta de Limón", "limon"),
    ("3/4", "torta", 3, 4, (255, 100, 200), "🍓", "Pastel de Fresa", "fresa"),
    ("1/5", "torta", 1, 5, (100, 200, 255), "🍊", "Tarta de Naranja", "naranja"),
    ("2/5", "torta", 2, 5, (255, 150, 50), "🍑", "Pastel de Durazno", "durazno"),
    ("3/5", "torta", 3, 5, (150, 255, 100), "🍈", "Tarta de Melón", "melon"),
    ("4/5", "torta", 4, 5, (255, 100, 150), "🍒", "Pastel de Cereza", "cereza"),
    ("1/6", "torta", 1, 6, (255, 200, 150), "🍉", "Tarta de Sandía", "sandia"),
    ("5/6", "torta", 5, 6, (200, 100, 255), "🍇", "Pastel de Uvas", "uva"),
    ("1/8", "torta", 1, 8, (255, 180, 100), "🥝", "Tarta de Kiwi", "kiwi"),
    ("3/8", "torta", 3, 8, (210, 150, 50), "🍌", "Pastel de Banana", "banana"),
    ("5/8", "torta", 5, 8, (100, 200, 150), "🍐", "Tarta de Pera", "pera"),
    ("7/8", "torta", 7, 8, (200, 130, 100), "🍪", "Pastel de Galleta", "galleta"),
]


class GestorFracciones:
    """Gestiona la selección aleatoria de fracciones"""
    
    def __init__(self):
        self.fracciones_usadas = []
    
    def seleccionar_aleatorias(self, cantidad):
        """Selecciona fracciones aleatorias sin repetir las últimas usadas"""
        disponibles = [f for f in BANCO_FRACCIONES if f not in self.fracciones_usadas[-4:]]
        
        if len(disponibles) < cantidad:
            self.fracciones_usadas = []
            disponibles = BANCO_FRACCIONES.copy()
        
        seleccionadas = random.sample(disponibles, cantidad)
        self.fracciones_usadas.extend(seleccionadas)
        return seleccionadas
    
    def reiniciar_historial(self):
        """Reinicia el historial de fracciones usadas"""
        self.fracciones_usadas = []