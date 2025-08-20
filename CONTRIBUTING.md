# Guía de Contribución - Shut Up Guy! 🎯

¡Gracias por tu interés en contribuir al proyecto **Shut Up Guy!**! Esta guía te ayudará a entender cómo puedes colaborar de manera efectiva.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Configuración del entorno de desarrollo](#configuración-del-entorno-de-desarrollo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Estándares de codificación](#estándares-de-codificación)
- [Proceso de contribución](#proceso-de-contribución)
- [Reportar bugs](#reportar-bugs)
- [Sugerir mejoras](#sugerir-mejoras)
- [Recursos adicionales](#recursos-adicionales)

## 🤝 Código de Conducta

Este proyecto se adhiere a un código de conducta que esperamos que todos los participantes respeten. Por favor, lee y sigue estas pautas:

- Sé respetuoso y constructivo en todas las interacciones
- Acepta críticas constructivas de manera profesional
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros de la comunidad

## 🛠️ ¿Cómo puedo contribuir?

Hay varias formas de contribuir a este proyecto:

### 🐛 Reportar Bugs
- Incluye pasos para reproducir el problema
- Proporciona información del sistema (OS, versión de Python, etc.)

### 💡 Sugerir Funcionalidades
- Abre un issue describiendo la funcionalidad propuesta
- Explica por qué sería útil para el juego
- Si es posible, proporciona mockups o ejemplos

### 🎨 Mejoras de Arte y Diseño
- Nuevos sprites para personajes
- Efectos visuales mejorados
- Nuevos fondos o texturas
- Mejoras en la interfaz de usuario

### 🔊 Audio y Música
- Nuevos efectos de sonido
- Música de fondo adicional
- Mejoras en la calidad del audio existente

### 🎮 Nuevas Funcionalidades
- Nuevos niveles de juego
- Modos de juego adicionales
- Mejoras en el sistema de control por gestos
- Sistema de puntuaciones online

### 📖 Documentación
- Mejoras en README
- Comentarios en el código
- Tutoriales de uso
- Guías de instalación

## 🚀 Configuración del entorno de desarrollo

### Prerrequisitos
- Python 3.7+ (recomendado 3.9+)
- Git
- Cámara web (para probar controles por gestos)

### Instalación

1. **Fork y clona el repositorio**
   ```bash
   git clone https://github.com/TU_USUARIO/shut-up-guy.git
   cd shut-up-guy
   ```

2. **Crear un entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Probar la instalación**
   ```bash
   python main.py
   ```

2. **Verificar que todo funciona**
   - El juego debe iniciar correctamente
   - Los menús deben ser navegables
   - Los controles por teclado deben funcionar
   - Si tienes cámara, prueba los controles por gestos

## 📁 Estructura del proyecto

```
shut-up-guy/
├── main.py                 # Punto de entrada del juego
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Documentación principal
├── CONTRIBUTING.md        # Esta guía
├── assets/                # Recursos del juego
│   ├── fonts/            # Fuentes tipográficas
│   ├── images/           # Sprites e imágenes
│   └── sounds/           # Efectos de sonido y música
├── data/                 # Datos de guardado
└── src/                  # Código fuente
    ├── app.py            # Clase principal del juego
    ├── config/           # Configuraciones y constantes
    ├── entity/           # Entidades del juego (jugador, enemigos, etc.)
    ├── scene/            # Escenas del juego (menú, gameplay, etc.)
    └── utils/            # Utilidades (audio, colisiones, etc.)
```

### Componentes principales

- **`src/app.py`**: Clase principal que maneja el bucle del juego
- **`src/scene/`**: Diferentes escenas (menú, juego, pausa, game over)
- **`src/entity/`**: Entidades del juego (jugador, obstáculos, proyectiles)
- **`src/utils/`**: Utilidades como manejo de audio, colisiones, entrada por cámara
- **`src/config/`**: Configuraciones, constantes y progreso del juego

## 📝 Estándares de codificación

### Estilo de código Python
- Usar nombres de variables y funciones descriptivos en español o inglés (mantener consistencia)
- Comentarios importantes en español
- Docstrings para clases y métodos complejos

### Ejemplo de estilo:
```python
class Player:
    """
    Representa al jugador principal del juego.
    
    Attributes:
        position (tuple): Posición actual del jugador (x, y)
        health (int): Vida actual del jugador
    """
    
    def __init__(self, initial_position):
        self.position = initial_position
        self.health = 100
        
    def move(self, direction):
        """Mueve al jugador en la dirección especificada."""
        # Lógica de movimiento aquí
        pass
```

### Organización de archivos
- Una clase por archivo cuando sea posible
- Nombres de archivos en minúsculas con guiones bajos
- Importaciones organizadas: librerías estándar, terceros, locales

### Assets y recursos
- Imágenes en formato PNG con transparencia
- Sonidos en formato MP3 o WAV
- Sprites con tamaño consistente (96x96px por defecto para entidades y 64x64px para proyectiles)
- Nombres descriptivos para todos los assets

## 🔄 Proceso de contribución

### 1. Antes de empezar
- Revisa los issues existentes para evitar trabajo duplicado
- Discute cambios grandes abriendo un issue primero
- Asegúrate de que tu idea se alinea con los objetivos del proyecto

### 2. Durante el desarrollo
- Crea una rama específica para tu funcionalidad o issue:
  ```bash
  git checkout -b feature/nombre-de-tu-feature
  git checkout -b feature/issue-123-nueva-funcionalidad
  ```
- Haz commits frecuentes y descriptivos:
  ```bash
  git commit -m "feat: añadir nuevo nivel con obstáculos móviles"
  ```
- Mantén tu rama actualizada con main:
  ```bash
  git fetch origin
  git rebase origin/main
  ```

### 3. Testing
- Prueba tu código exhaustivamente
- Verifica que no rompas funcionalidades existentes
- Prueba en diferentes resoluciones si es relevante
- Si añades controles por gestos, prueba con diferentes condiciones de iluminación

### 4. Crear Pull Request
- Título descriptivo del cambio
- Descripción detallada de qué hace tu contribución
- Screenshots o videos si hay cambios visuales
- Lista de cambios principales
- Referencias a issues relacionados

### Ejemplo de mensaje de commit:
```
feat: añadir modo de dificultad extrema

- Añadido nuevo modo de dificultad con enemigos más rápidos
- Incrementado spawn rate en 50%
- Reducido tiempo de reacción del jugador
- Actualizada interfaz para mostrar nueva dificultad

Closes #23
```

## 🐛 Reportar bugs

Para reportar un bug, por favor incluye:

### Información del sistema
- Sistema operativo y versión
- Versión de Python
- Versión de las dependencias principales

### Descripción del problema
- ¿Qué esperabas que pasara?
- ¿Qué pasó realmente?
- ¿Cuándo ocurre el problema?

### Pasos para reproducir
1. Paso 1
2. Paso 2
3. Paso 3
4. El error ocurre

### Información adicional
- Logs de error si están disponibles
- Screenshots o videos si es visual
- ¿Ocurre consistentemente o esporádicamente?

## 💡 Sugerir mejoras

Cuando sugieras una mejora, considera:

### Justificación
- ¿Por qué sería útil esta mejora?
- ¿Cómo mejora la experiencia del jugador?
- ¿Se alinea con los objetivos del juego?

### Implementación
- ¿Cómo podría implementarse?
- ¿Qué recursos se necesitarían?
- ¿Afectaría el rendimiento?

### Ejemplos
- Mockups o sketches si es visual
- Ejemplos de otros juegos que implementen algo similar
- Casos de uso específicos

## 🎨 Contribuir con Assets

### Imágenes y Sprites
- Formato: PNG con transparencia
- Tamaño: Múltiplos de 96px para mantener consistencia
- Estilo: Pixel art con paleta de colores cohesiva
- Nombre: Descriptivo y en inglés (ej: `teacher_shooting.png`)

### Audio
- Formato: MP3 para música, WAV para efectos
- Calidad: 44.1kHz, stereo
- Duración: Efectos cortos (<2s), música puede ser más larga
- Volumen: Normalizado para evitar picos

### Fuentes
- Solo fuentes con licencia libre
- Formato TTF preferiblemente
- Estilo que coincida con la estética del juego

## 🧪 Testing y Quality Assurance

### Testing manual
- Prueba tu código en diferentes escenarios
- Verifica compatibilidad con controles de teclado y gestos
- Prueba en diferentes resoluciones de pantalla
- Verifica que los sonidos funcionen correctamente

### Performance
- El juego debe mantener 60 FPS en hardware moderno
- Evita memory leaks en bucles largos
- Optimiza assets grandes si es necesario

### Accesibilidad
- Controles alternativos para usuarios con limitaciones
- Contrastes de color adecuados
- Tamaños de texto legibles

## 🤖 Automatización y CI/CD

Actualmente no tenemos CI/CD configurado, pero sería una gran contribución:

- GitHub Actions para testing automático
- Validación de estilo de código
- Builds automáticos para diferentes plataformas
- Testing de regresión automático

## 📚 Recursos adicionales

### Pygame
- [Documentación oficial de Pygame](https://www.pygame.org/docs/)
- [Tutoriales de Pygame](https://realpython.com/pygame-a-primer/)

### Computer Vision (MediaPipe)
- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)

## 📞 Contacto

¿Tienes preguntas sobre cómo contribuir?

**Autor**: Alexander Nieves  
**Email**: ganieves@espol.edu.ec

### Canales de comunicación
- Abre un issue para discusiones públicas
- Envía email para consultas específicas
- Revisa issues existentes antes de preguntar

## 🙏 Reconocimientos

Todos los contribuyentes serán reconocidos en:
- README principal del proyecto
- Sección de créditos en el juego
- Lista de contribuyentes en GitHub

---

¡Gracias por tu interés en mejorar **Shut Up Guy!**! Esperamos tus contribuciones 🚀
