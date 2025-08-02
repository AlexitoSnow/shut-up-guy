# Configuraciones del juego
# Maneja configuraciones modificables como volumen,
# controles personalizados, dificultad, etc.
import json
import os
from os.path import join, dirname, abspath

class Settings:
    def __init__(self):
        # Crear ruta absoluta para el archivo de configuración
        current_dir = dirname(abspath(__file__))
        project_root = dirname(dirname(current_dir))
        data_dir = join(project_root, 'data')
        self.settings_file = join(data_dir, 'settings.json')
        
        # Asegurar que el directorio existe
        os.makedirs(data_dir, exist_ok=True)
        
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                self.volume = settings.get('volume', 0.5)
                self.difficulty = settings.get('difficulty', 'normal')
                self.controls = settings.get('controls', ['standard', 'dynamic', 'both'])
                self.select_controls = settings.get('select_controls', 'standard')
                self.camera_index = settings.get('camera_index', 0)
        except FileNotFoundError:
            self.volume = 0.5
            self.difficulty = 'normal'
            self.controls = ['standard', 'dynamic', 'both']
            self.select_controls = 'standard'
            self.camera_index = 0
            self.save_settings()

    def save_settings(self):
        settings = {
            'volume': self.volume,
            'difficulty': self.difficulty,
            'controls': self.controls,
            'select_controls': self.select_controls,
            'camera_index': self.camera_index
        }
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file, indent=4)