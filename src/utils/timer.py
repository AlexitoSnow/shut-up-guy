import pygame


class Timer:
    def __init__(self, duration, func = None, repeat = False, autostart = False, reverse = False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat
        self.reverse = reverse

        if autostart:
            self.activate()

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()

    def get_time_in_seconds(self):
        if self.active:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if self.reverse:
                remaining = max(0, (self.duration - elapsed_time) // 1000)
                return remaining
            return elapsed_time // 1000
        return self.duration // 1000 if self.reverse else 0

    def pause(self):
        if self.active:
            self.remaining = self.duration - (pygame.time.get_ticks() - self.start_time)
            self.deactivate()

    def resume(self):
        if not self.active and hasattr(self, 'remaining') and self.remaining > 0:
            self.duration = self.remaining
            self.activate()
            del self.remaining