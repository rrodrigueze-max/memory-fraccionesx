# AGENTS

## Project overview
- Repositorio de un juego educativo en Python usando `pygame`.
- El juego es un "Memory de Fracciones" con cartas que muestran fracciones en texto o como tortas.
- No hay un archivo `requirements.txt` ni pruebas automatizadas en el repositorio.

## Ejecución
- Punto de entrada principal: `main.py`.
- Comando de ejecución desde la raíz del repositorio:
  ```bash
  python main.py
  ```
- Dependencia principal: `pygame`.
- El proyecto incluye una carpeta `venv/` y `.venv/`; usa el entorno virtual apropiado si está configurado.

## Componentes clave
- `main.py`: inicializa `pygame`, muestra la historia introductoria y ejecuta el bucle principal.
- `config.py`: define constantes de pantalla, colores y la configuración de niveles (`NIVELES_CONFIG`).
- `classes/juego.py`: clase principal `JuegoMemory` que controla el estado del juego, eventos, lógica de niveles y renderizado.
- `classes/tarjeta.py`: clase `Tarjeta` para representar cartas individuales y dibujar su reverso/contenido.
- `pantalla_historia.py`: pantalla de historia / inicio del juego.
- `pantalla_final.py`: pantalla de fin del juego.
- `utils/sonidos.py`: gestión de efectos de sonido.
- `utils/fracciones.py`: gestión de fracciones y selección aleatoria de pares.
- `utils/dibujos.py`: utilidades de dibujo, incluido el renderizado de las tortas.

## Convenciones de desarrollo
- El código usa comentarios y nombres de variables principalmente en español; sigue esa convención.
- Mantén la lógica central del juego dentro de `JuegoMemory` y evita mover el bucle principal fuera de `main.py`.
- Usa constantes de `config.py` cuando sea posible para colores, tamaños de pantalla y tiempos.
- Para agregar un nuevo nivel, extiende `NIVELES_CONFIG` en `config.py` y mantén la creación/posicionamiento de cartas en `JuegoMemory.iniciar_nivel()` y `_posicionar_cartas()`.
- No modifiques la carpeta `build/` a menos que sepas que es parte de un proceso de construcción específico.

## Información útil para agentes
- No hay documentación externa en el repositorio; este archivo debe ser la referencia principal para entender cómo empezar.
- Si agregas nuevas características, actualiza también `config.py` y documenta los cambios en comentarios claros dentro del código.
- El proyecto tiene una interfaz gráfica y depende de eventos del ratón/teclado. Comprueba que los cambios no rompan la lógica de `manejar_eventos()`, `actualizar()` y `dibujar()`.
