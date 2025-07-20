# Escena principal del juego
# Contiene la lógica principal del gameplay:
# spawning de enemigos, manejo de colisiones, puntuación, etc.
from random import choice

import pygame
from pygame.locals import QUIT

from config import *
from entity import Obstacle, Player, ENEMY, FLY
from scene.scene import Scene
from utils import Timer, CameraInputHandler


class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Groups
        self.character = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()

        # Sprites
        test_font = pygame.font.Font(None, 36)
        self.text_surface = test_font.render(APP_NAME, False, BLACK)
        self.text_rect = self.text_surface.get_rect(center = (SCREEN_WIDTH / 2, 50))

        # Timers
        self.obstacle_timer_gen = Timer(1400, self.spawn_enemy, True, True)

        self.load_images()

        # Input handlers
        self.cam_handler = CameraInputHandler()
        self.character.add(Player([self.char_run_1, self.char_run_2], self.cam_handler))

    def init(self):
        self.cam_handler.start()

    def handle_events(self, events):
        self.collisions()
        for event in events:
            if event.type == QUIT:
                self.cam_handler.stop()

    def update(self):
        self.obstacle_timer_gen.update()
        self.character.update()
        self.character.sprite.projectile_group.update()
        self.obstacles.update()

    def draw(self, screen):
        screen.blit(self.park_background, (0, 0))
        pygame.draw.rect(screen, 'Gold', self.text_rect)
        pygame.draw.rect(screen, 'White', self.text_rect, 10)
        screen.blit(self.text_surface, self.text_rect)
        self.character.draw(screen)
        self.character.sprite.projectile_group.draw(screen)
        self.obstacles.draw(screen)
        # Draw player, enemies, score, etc.

    def load_images(self):
        self.park_background = pygame.image.load(join(IMAGES, 'park.png')).convert()
        self.park_background = pygame.transform.scale(self.park_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.fly_1 = pygame.image.load(join(IMAGES, 'fly_1.png')).convert_alpha()
        self.fly_2 = pygame.image.load(join(IMAGES, 'fly_2.png')).convert_alpha()
        self.fly_1 = pygame.transform.scale2x(self.fly_1)
        self.fly_2 = pygame.transform.scale2x(self.fly_2)

        self.enemy_1 = pygame.image.load(join(IMAGES, 'enemy_1.png')).convert_alpha()
        self.enemy_2 = pygame.image.load(join(IMAGES, 'enemy_2.png')).convert_alpha()
        self.enemy_1 = pygame.transform.scale2x(self.enemy_1)
        self.enemy_2 = pygame.transform.scale2x(self.enemy_2)

        self.char_run_1 = pygame.image.load(join(IMAGES, 'char_run_1.png')).convert_alpha()
        self.char_run_1 = pygame.transform.scale2x(self.char_run_1)
        self.char_run_2 = pygame.image.load(join(IMAGES, 'char_run_2.png')).convert_alpha()
        self.char_run_2 = pygame.transform.scale2x(self.char_run_2)

    def collisions(self) -> bool:
        for obstacle in self.obstacles:
            if pygame.sprite.spritecollide(obstacle, self.character.sprite.projectile_group, True):
                obstacle.kill()

    def spawn_enemy(self):
        enemy_type = choice([FLY, ENEMY])
        if enemy_type == FLY:
            surfaces = [self.fly_1, self.fly_2]
        else:
            surfaces = [self.enemy_1, self.enemy_2]
        self.obstacles.add(Obstacle(surfaces=surfaces, enemy_type=enemy_type))