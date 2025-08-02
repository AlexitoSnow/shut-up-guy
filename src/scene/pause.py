# Escena de pausa
# Permite pausar el juego y mostrar un menú de opciones
# como continuar, reiniciar, configuraciones o volver al menú
import pygame

from .base_scene import Scene
from ..utils import Button, Text


class PauseScene(Scene):
    def __init__(self, game, on_resume = None):
        super().__init__(game)
        self.game = game
        self.on_resume = on_resume if on_resume else lambda: None

        self.title = Text("PAUSA", 48, (game.screen.get_width() // 2, 150))
        self.resume_button = Button("Continuar", (game.screen.get_width() // 2, 300), 48, self.on_resume, text_color=(255, 255, 0))
        self.quit_button = Button("Salir", (game.screen.get_width() // 2, 350), 48, self.on_tap_quit, text_color=(255, 255, 0))
        self.container_surf = pygame.Surface((600, 500))
        self.container_surf.set_alpha(200)
        self.container_surf.fill((0, 0, 0))

    def on_tap_quit(self):
        self.game.change_scene('menu')

    def update(self):
        cursor_type = pygame.SYSTEM_CURSOR_ARROW
        buttons = [self.resume_button, self.quit_button]
        for button in buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                cursor_type = pygame.SYSTEM_CURSOR_HAND
                if pygame.mouse.get_pressed()[0]:
                    button.on_tap()
        pygame.mouse.set_cursor(cursor_type)

    def draw(self, screen):
        # Dibujar fondo semi-transparente
        screen.blit(self.container_surf, (screen.get_width() // 2 - 300, screen.get_height() // 2 - 250))

        # Dibujar título y botones
        screen.blit(self.title.surf(), self.title.rect)
        self.resume_button.draw(screen)
        self.quit_button.draw(screen)