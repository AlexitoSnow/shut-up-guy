# Escena del menú principal
# Interfaz de inicio del juego con opciones como:
# jugar, configuraciones, puntuaciones altas, salir
import pygame

from src.scene.scene import Scene


class MenuScene(Scene):
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 48)
        self.title = self.font.render("Shut Up Guy", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.game.screen.get_width() // 2, 150))
        self.play_button = self.font.render("¡JUGAR!", True, (255, 255, 0))
        self.play_button_rect = self.play_button.get_rect(center=(self.game.screen.get_width() // 2, 300))

    def handle_events(self, events):
        pass

    def update(self):
        if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:
                self.game.change_scene('game')
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.play_button, self.play_button_rect)