# Sistema de detección de colisiones
# Implementa algoritmos eficientes para detectar colisiones
# entre sprites, rectángulos y formas circulares
import pygame

def collide_between(group_1: list, group_2: list, do_kill_1 = False, do_kill_2 = False, on_collide = None):
    for sprite in group_1:
        if pygame.sprite.spritecollide(sprite, group_2, do_kill_2):
            if do_kill_1: sprite.kill()
            on_collide()