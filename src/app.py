import pygame
from pygame.locals import *

from .config.constants import *
from .config import Settings, Progress
from .scene import MenuScene, GameplayScene, LevelsScene, GameOverScene
from .utils import ResourceManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(APP_NAME)

        # Inicializar y reproducir música de fondo
        pygame.mixer.music.load('assets/sounds/background.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 significa reproducción infinita

        self.clock = pygame.time.Clock()
        self.running = True

        self.settings = Settings()
        self.resources = ResourceManager()
        self.progress = Progress()

        # Guarda las clases, no las instancias
        self.scenes = {
            'menu': MenuScene,
            'game': GameplayScene,
            'levels': LevelsScene,
            'gameover': GameOverScene,
        }

        self.current_scene = None


    def change_scene(self, scene_name, **kwargs):
        if scene_name in self.scenes:
            # Instancia la escena bajo demanda
            self.current_scene = self.scenes[scene_name](self, **kwargs)

    def run(self):
        self.change_scene('menu')
        while self.running:
            events = pygame.event.get()
            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            for event in events:
                if event.type == QUIT:
                    self.running = False
        pygame.quit()