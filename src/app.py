import pygame
from pygame.locals import *

from config import *
from entity import *
from scene import MenuScene, GameplayScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(APP_NAME)

        self.clock = pygame.time.Clock()
        self.running = True
        self.settings = Settings()

        self.scenes = {
            'menu': MenuScene(self),
            'game': GameplayScene(self),
        }

        self.current_scene = self.scenes['menu']


    def change_scene(self,  scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.init()

    def run(self):
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


if __name__ == "__main__":
    Game().run()