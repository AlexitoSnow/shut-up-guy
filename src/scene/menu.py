# Escena del menú principal
# Interfaz de inicio del juego con opciones como:
# jugar, configuraciones, puntuaciones altas, salir
import pygame

from .base_scene import Scene
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, ORIGINAL_ENTITY_SIZE, ENTITY_SIZE, WHITE
from ..utils import Button, Text


class MenuScene(Scene):
    def __init__(self, game):
        self.game = game

        # Cargar y escalar fondo
        background = self.game.resources.load_image('back_1_5.png', 'background')
        self.background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Título
        self.title = Text("Shut Up Guy", 48, (SCREEN_WIDTH // 2, 150))
        self.play_button = Button('¡JUGAR!', (SCREEN_WIDTH // 2, 300), 48, text_color=(255, 255, 0), bg_color=WHITE)
        self.difficulty = Button(str(game.settings.difficulty).upper(), (SCREEN_WIDTH // 2, 50), 30, text_color=(255, 255, 0), bg_color=WHITE)

        # Control icon y su configuración
        self.control_frames = []
        self.current_control = self.game.settings.select_controls
        self.control_index = {
            'standard': 0,
            'dynamic': 1,
            'both': 2
        }[self.current_control]

        # Cargar frames del ícono de movimiento
        movement_icon = self.game.resources.load_image('movement_icon.png', 'misc')
        # Extraer los 3 frames (32x32 cada uno)
        for i in range(3):
            frame = pygame.Surface((32, 32), pygame.SRCALPHA)
            frame.blit(movement_icon, (0, 0), (i * 32, 0, 32, 32))
            frame = pygame.transform.scale(frame, (64, 64))  # Escalar a 64x64 para mejor visibilidad
            self.control_frames.append(frame)

        # Posicionar el ícono en la esquina inferior
        self.control_rect = self.control_frames[0].get_rect(midbottom=(50, SCREEN_HEIGHT - 50))

        width, height = ORIGINAL_ENTITY_SIZE

        # Standing tiene 3 frames
        player_sheet = game.resources.load_image('teacher_standing.png', 'teacher')
        self.player_frames = []
        for i in range(3):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(player_sheet, (0, 0), (i * width, 0, width, height))
            # Escalar al tamaño de renderizado
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.player_frames.append(frame)
        self.teacher = self.player_frames[0]
        self.teacher_rect = self.teacher.get_rect(midbottom=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50))
        self.teacher_index = 0

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Click izquierdo liberado
                if self.play_button.rect.collidepoint(mouse_pos):
                    self.game.change_scene('levels')
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif self.difficulty.rect.collidepoint(mouse_pos):
                    self.toggle_difficulty()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif self.control_rect.collidepoint(mouse_pos):
                    self.cycle_control_mode()

        # Actualizar cursor
        if self.play_button.rect.collidepoint(mouse_pos) or self.control_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def cycle_control_mode(self):
        # Ciclar entre los modos de control
        controls = ['standard', 'dynamic', 'both']
        current_index = controls.index(self.current_control)
        next_index = (current_index + 1) % 3
        self.current_control = controls[next_index]
        self.control_index = next_index
        # Guardar en configuración
        self.game.settings.select_controls = self.current_control
        self.game.settings.save_settings()

    def draw(self, screen):
        # Dibujar fondo
        screen.blit(self.background, (0, 0))
        screen.blit(self.title.surf(), self.title.rect)
        self.play_button.draw(screen)
        self.difficulty.draw(screen)
        screen.blit(self.control_frames[self.control_index], self.control_rect)
        screen.blit(self.teacher, self.teacher_rect)

    def update(self):
        self.teacher_index = (self.teacher_index + 0.1) % 3
        self.teacher = self.player_frames[int(self.teacher_index)]

    def toggle_difficulty(self):
        # Cambiar dificultad
        if self.game.settings.difficulty == 'easy':
            self.game.settings.difficulty = 'medium'
        elif self.game.settings.difficulty == 'medium':
            self.game.settings.difficulty = 'hard'
        else:
            self.game.settings.difficulty = 'easy'
        self.game.settings.save_settings()
        self.difficulty = Button(str(self.game.settings.difficulty).upper(), (SCREEN_WIDTH // 2, 50), 30, text_color=(255, 255, 0), bg_color=WHITE)
