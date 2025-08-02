# Manejo de recursos (imágenes, sonidos, fuentes)
# Carga y gestiona todos los assets del juego de forma eficiente
# incluye caché y optimización de recursos
import pygame
import os

from ..config.constants import *

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, name, subdir):
        if name not in self.images:
            if subdir is None:
                path = os.path.join(IMAGES, name)
            else:
                path = os.path.join(IMAGES, subdir, name)
            self.images[name] = pygame.image.load(path).convert_alpha()
        return self.images[name]

    def load_sound(self, name, subdir):
        if name not in self.sounds:
            path = os.path.join(SOUNDS, subdir, name)
            self.sounds[name] = pygame.mixer.Sound(path)
        return self.sounds[name]

    def load_font(self, name, size, subdir):
        key = f"{name}_{size}"
        if key not in self.fonts:
            path = os.path.join(FONTS, subdir, name)
            self.fonts[key] = pygame.font.Font(path, size)
        return self.fonts[key]

    def load_images(self, names, subdir = None):
        images = []
        for name in names:
            images.append(self.load_image(name, subdir))
        return images

    def load_tile_set(self, name, tile_width, tile_height, subdir = None):
        tiles = []
        if subdir is None:
            path = os.path.join(IMAGES, name)
        else:
            path = os.path.join(IMAGES, subdir, name)
        tileset = pygame.image.load(path).convert_alpha()
        tileset_width, tileset_height = tileset.get_size()
        for y in range(0, tileset_height, tile_height):
            for x in range(0, tileset_width, tile_width):
                rect = pygame.Rect(x, y, tile_width, tile_height)
                tile = tileset.subsurface(rect).copy()
                tiles.append(tile)
        return tiles