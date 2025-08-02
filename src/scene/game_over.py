# Escena de game over
# Pantalla que se muestra cuando el jugador pierde,
# con opciones para reiniciar, volver al menú o salir
import pygame

from .base_scene import Scene
from ..config import WHITE
from ..utils import Button, Text


class GameOverScene(Scene):
    def __init__(self, game, level=None, results=None):
        super().__init__(game)
        self.game = game
        self.level = level
        self.results = results

        # Calcular score y estado de victoria
        self.score = self.calculate_score()
        self.victory = self.results['killed_enemies'] >= self.level.enemy_count

        # Preparar textos
        title_text = "¡VICTORIA!" if self.victory else "GAME OVER"
        self.title = Text(title_text, 48, (game.screen.get_width() // 2, 150))

        # Crear textos de resultados
        score_text = f"Score: {self.score}"
        time_text = f"Tiempo restante: {self.results['time_remaining']} segundos"
        kills_text = f"Enemigos eliminados: {self.results['killed_enemies']}/{self.level.enemy_count}"
        shots_text = f"Disparos realizados: {self.results['shots_fired']}"

        y_pos = 200
        self.score_display = Text(score_text, 36, (game.screen.get_width() // 2, y_pos))
        self.time_display = Text(time_text, 36, (game.screen.get_width() // 2, y_pos + 50))
        self.kills_display = Text(kills_text, 36, (game.screen.get_width() // 2, y_pos + 100))
        self.shots_display = Text(shots_text, 36, (game.screen.get_width() // 2, y_pos + 150))

        # Botón de continuar
        self.resume_button = Button("Continuar", (game.screen.get_width() // 2, y_pos + 250), 48, self.on_tap_quit)

        # Fondo semi-transparente
        self.container_surf = pygame.Surface((600, 500))
        self.container_surf.set_alpha(200)
        self.container_surf.fill((0, 0, 0))

    def calculate_score(self):
        # Base score por enemigos eliminados
        kill_score = self.results['killed_enemies'] * 100

        # Bonus por tiempo restante
        time_bonus = self.results['time_remaining'] * 10

        # Penalización por disparos usados (si no son infinitos)
        shot_penalty = 0
        if self.results['bullet_count'] != -1:
            shot_penalty = self.results['shots_fired'] * 5

        # Score final
        return max(0, kill_score + time_bonus - shot_penalty)

    def on_tap_quit(self):
        self.game.change_scene('levels')

    def update(self):
        cursor_type = pygame.SYSTEM_CURSOR_ARROW
        if self.resume_button.rect.collidepoint(pygame.mouse.get_pos()):
            cursor_type = pygame.SYSTEM_CURSOR_HAND
            if pygame.mouse.get_pressed()[0]:
                self.resume_button.on_tap()
                cursor_type = pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor_type)

    def draw(self, screen):
        # Dibujar fondo semi-transparente
        screen.blit(self.container_surf, (screen.get_width() // 2 - 300, screen.get_height() // 2 - 250))

        # Dibujar todos los textos
        screen.blit(self.title.surf(), self.title.rect)
        screen.blit(self.score_display.surf(), self.score_display.rect)
        screen.blit(self.time_display.surf(), self.time_display.rect)
        screen.blit(self.kills_display.surf(), self.kills_display.rect)
        screen.blit(self.shots_display.surf(), self.shots_display.rect)

        # Dibujar botón
        self.resume_button.draw(screen)