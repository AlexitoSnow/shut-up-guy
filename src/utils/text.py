import pygame
import os
from ..config.constants import FONTS, MAIN_FONT


class Text:
    def __init__(self, content='', size=36, pos=(0, 0), font_name=MAIN_FONT, color=(255, 255, 255), antialias=True):
        try:
            font_path = os.path.join(FONTS, font_name)
            self.font = pygame.font.Font(font_path, size)
        except (FileNotFoundError, pygame.error):
            print(f"Warning: Font {font_name} not found, using default system font")
            self.font = pygame.font.Font(None, size)

        self.position = pos
        self.content = content
        self.color = color
        self.antialias = antialias
        self.surface = None
        self.rect = None
        self.update_text(content)

    def surf(self, text=None):
        if text is not None:
            self.update_text(text)
        return self.surface

    def update_text(self, text):
        if text is None:
            text = ''
        self.content = text
        self.surface = self.font.render(text, self.antialias, self.color)
        self.rect = self.surface.get_rect(center=self.position)
