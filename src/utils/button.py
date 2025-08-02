import pygame
from os.path import join
from ..config.constants import FONTS, MAIN_FONT

class Button:
    def __init__(self, text, pos, size, on_tap=None, text_color=(255, 255, 255), bg_color=None):
        self.text = text
        self.font = pygame.font.Font(join(FONTS, MAIN_FONT), size)
        self.on_tap = on_tap
        self.bg_color = bg_color
        self.text_color = text_color

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=pos)

        if self.bg_color:
            # Crea una superficie más grande que el texto para el fondo
            padding_x, padding_y = 30, 20
            width = self.text_rect.width + padding_x
            height = self.text_rect.height + padding_y
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(self.bg_color)
            self.rect = self.image.get_rect(center=pos)
            self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        else:
            self.image = self.text_surf
            self.rect = self.image.get_rect(center=pos)
            self.text_rect = self.rect

    def draw(self, screen):
        if self.bg_color:
            screen.blit(self.image, self.rect)
            screen.blit(self.text_surf, self.text_rect)
        else:
            screen.blit(self.text_surf, self.rect)