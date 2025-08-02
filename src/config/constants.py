from os.path import join, dirname, abspath

# Obtener la ruta raíz del proyecto (2 niveles arriba de este archivo)
ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))

# Constantes del juego
# Define todas las constantes como dimensiones de pantalla,
# velocidades, colores, teclas de control, etc.
APP_NAME = "Shut up, guy!"

MAIN_FONT = 'VCR_OSD_MONO_1.001.ttf'  # Fuente principal del juego

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GROUND = 500

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Rutas absolutas para los recursos
FONTS = join(ROOT_DIR, 'assets', 'fonts')
SOUNDS = join(ROOT_DIR, 'assets', 'sounds')
IMAGES = join(ROOT_DIR, 'assets', 'images')
DATA = join(ROOT_DIR, 'data')

# Tamaños originales de los recursos
ORIGINAL_ENTITY_SIZE = (96, 96)  # Tamaño original de las entidades en píxeles
ORIGINAL_PROJECTILE_SIZE = (64, 64)  # Tamaño original de los proyectiles en píxeles

# Tamaños de renderizado (más pequeños)
ENTITY_SIZE = (64, 64)  # Tamaño de renderizado de las entidades
PROJECTILE_SIZE = (32, 32)  # Tamaño de renderizado de los proyectiles

# Dimensiones específicas de UI
TIMER_SIZE = (96, 96)  # Aumentado de 64x64 a 96x96
TIMER_TEXT_AREA = (84, 48)  # Área útil del timer para el texto (proporcionalmente más grande)
TIMER_POSITION = (100, 60)  # Ajustando posición para el nuevo tamaño

LEVEL_MAX = 15 # Número máximo de niveles