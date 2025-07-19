# Configuraciones del juego
# Maneja configuraciones modificables como volumen,
# controles personalizados, dificultad, etc.
import json
from os.path import join

from src.config import DATA

class Settings:
    def __init__(self):
        self.settings_file = join(DATA, 'settings.json')
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                self.volume = settings.get('volume', 0.5)
                self.difficulty = settings.get('difficulty', 'normal')
                self.controls = settings.get('controls', ['standard', 'dynamic', 'both'])
                self.select_controls = settings.get('select_controls', 'standard')
        except FileNotFoundError:
            self.volume = 0.5
            self.difficulty = 'normal'
            self.controls = ['standard', 'dynamic', 'both']
            self.select_controls = 'standard'
            self.save_settings()

    def save_settings(self):
        settings = {
            'volume': self.volume,
            'difficulty': self.difficulty,
            'controls': self.controls,
            'select_controls': self.select_controls
        }
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file, indent=4)