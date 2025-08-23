# Shut Up Guy! 🎯

## Índice

- [Descripción](#descripción)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Instrucciones de Juego](#instrucciones-de-juego)
- [Configuración del Juego](#configuración-del-juego)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Autor](#autor)

## Descripción

**Shut Up Guy!** Es un juego de acción desarrollado en Python usando Pygame, donde controlas a un profesor que debe mantener el orden en el aula disparando proyectiles a los estudiantes ruidosos. El juego cuenta con controles tradicionales de teclado y un innovador sistema de control por cámara usando reconocimiento de gestos con las manos.

### Características principales:
- **15 niveles progresivos** con dificultad creciente
- **Sistema de control dual**: teclado tradicional o control por gestos con cámara web
- **Reconocimiento de gestos**: usa MediaPipe para detectar movimientos de manos
- **Múltiples dificultades**: Easy, Medium, Hard
- **Sistema de progreso**: guarda automáticamente el progreso del jugador
- **Efectos visuales y sonoros**: fondos dinámicos, animaciones y efectos de sonido
- **Interfaz intuitiva**: menús fáciles de navegar con soporte de mouse

## Requisitos del Sistema

### Versión de Python
- **Python 3.7 o superior** (recomendado Python 3.9+)

### Dependencias
Las siguientes librerías son necesarias para ejecutar el juego:

```
pygame-ce >= 2.0.0
opencv-python >= 4.5.0
mediapipe >= 0.9.0
SpeechRecognition >= 3.8.0
pyaudio >= 0.2.11
```

### Requisitos adicionales para control por cámara:
- Cámara web funcional (USB o integrada)
- Buena iluminación para el reconocimiento de gestos
- Espacio suficiente para mover las manos frente a la cámara

## Instalación y Ejecución

### 1. Clonar o descargar el proyecto
```bash
git clone https://github.com/AlexitoSnow/shut-up-guy.git
cd shut-up-guy
```

### 2. Crear un entorno virtual (recomendado)
```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el juego
```bash
python main.py
```

Alternativamente, si usas VSCode, hay una configuración de depuración lista para usar en el archivo `.vscode/launch.json`, que puedes utilizar para ejecutar presionando F5.

## Instrucciones de Juego

### Objetivo
Elimina a todos los estudiantes ruidosos en cada nivel antes de que se agote el tiempo o te quedes sin munición.

### Controles

#### Controles de Teclado (Modo Standard):
- **Flecha Izquierda / A**: Mover hacia la izquierda
- **Flecha Derecha / D**: Mover hacia la derecha  
- **Barra Espaciadora**: Disparar
- **ESC**: Pausar/Reanudar el juego

#### Controles por Cámara (Modo Dynamic):
1. **Movimiento**: Extiende tu dedo índice y muévelo hacia la izquierda o derecha
2. **Disparo**: Extiende tu pulgar mientras mantienes el índice extendido
3. **Posición neutral**: Mantén la mano cerrada para no moverte

#### Modo Both:
Puedes usar ambos tipos de control simultáneamente.

### Mecánicas del Juego

#### Sistema de Niveles:
- **15 niveles** organizados en 3 grupos de 5 niveles cada uno
- La dificultad aumenta progresivamente:
  - Más enemigos por nivel
  - Menos tiempo disponible
  - Enemigos más rápidos
  - Menor tiempo de vida de los enemigos

#### Elementos de Interfaz:
- **Timer**: Muestra el tiempo restante (formato MM:SS)
- **Contador de munición**: Indica las balas restantes
- **Contador de enemigos**: Muestra enemigos restantes en la esquina superior derecha

## Configuración del Juego

### Selección de Dificultad:
- **Easy**: Más tiempo, menos enemigos, munición ilimitada
- **Medium**: Configuración balanceada, munición suficiente para matar a todos los enemigos
- **Hard**: Menos tiempo, más enemigos, mayor velocidad, munición exacta para matar a todos los enemigos

### Configuración de Cámara:
- El juego detecta automáticamente las cámaras disponibles
- Puedes cambiar entre cámaras desde el archivo de configuración, el atributo camera_index: [settings.json](data/settings.json)
  - __Nota__: El archivo es autogenerado al iniciar el juego por primera vez
- Si hay problemas con la cámara, el juego utilizará automáticamente la cámara por defecto

## Estructura del Proyecto

```
shut-up-guy/
├── main.py                 # Punto de entrada del juego
├── requirements.txt        # Dependencias de Python
├── assets/                 # Recursos del juego
│   ├── fonts/             # Fuentes tipográficas
│   ├── images/            # Sprites y fondos
│   └── sounds/            # Efectos de sonido y música
├── data/                  # Datos de configuración y progreso
├── src/                   # Código fuente principal
│   ├── config/           # Configuraciones y constantes
│   ├── entity/           # Entidades del juego (jugador, enemigos)
│   ├── scene/            # Escenas del juego (menú, gameplay)
│   └── utils/            # Utilidades (audio, botones, colisiones)
```

## Autor

**Alexander Nieves**
- Email: ganieves@espol.edu.ec

---